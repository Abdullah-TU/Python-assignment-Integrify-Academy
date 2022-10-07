# Libraries
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.models import add_new_todo_item , get_todo_item_by_id,get_todo_item_using_filter,get_all_todo_items_against_userId,update_todo_item,delete_todo_item_from_db
from src.constants.Constants import base_url
from src.DTO.ServerResponseDTO import get_server_response

# Todo items related blueprint.
todosController = Blueprint("todosController", __name__, url_prefix=base_url)


@todosController.route('/todos', methods=['POST', 'GET'])

# Required access token
@jwt_required()
def Todos():
    # Get current user's identity
    current_user = get_jwt_identity()
    status_list = ['OnGoing', 'NotStarted', 'Completed']
    # Post request to add new item in to do list
    if request.method == 'POST':

        name = request.json.get('name', '')
        if name == '':
            return get_server_response(status=0, msg="item should have a name in order to add todo item")
        # Optional description, default empty
        description = request.json.get('description', '')

        # If not provided default status is set to NotStarted
        status_value = request.json.get('status', 'NotStarted')

        if status_value not in status_list:
            return get_server_response(status=0, msg="value must be from 'OnGoing','NotStarted','Completed'")

        add_new_todo_item(name, description, current_user, status_value)

        return get_server_response(status=1, msg="Item has been added in todo list")
    # If request is not POST, it must be GET
    else:

        # If there is any status in query parameter
        if 'status' in request.args:
            status_value = request.args.get('status', type=str)
            # If status parameter is present, check if is in allowed STATUS from database
            if status_value in status_list:
                todo_items = get_todo_item_using_filter(current_user, status_value)

            # If status was not in the allowed STATUS ENUM in the database
            else:
                return get_server_response(status=0, msg="status must be from 'OnGoing','NotStarted','Completed'")

        # If no parameter named 'status' is given return all items
        else:
            todo_items = get_all_todo_items_against_userId(current_user)
        # Collect all requested items in an array
        data = []
        for todo_item in todo_items:
            data.append(
                {'id': todo_item.Id,
                 'user': todo_item.UserId,
                 'name': todo_item.Name,
                 'description': todo_item.Description,
                 'status': todo_item.status
                 }
            )
        return get_server_response(status=1, msg="", data=data)


@todosController.put("/todos:<int:id>")
@jwt_required()
def updateTodoItem(id):
    # Get current user's identity
    current_user = get_jwt_identity()
    todo_item = get_todo_item_by_id(current_user, id)

    # If todo item is not found for the current user.
    if not todo_item:
        return get_server_response(status=1, msg="Item not found")

    # If item is found we can update its fields.
    else:

        # If no name is provided, keeps original name
        name = request.json.get('name', '')

        # Optional description, if not provided keeps original
        description = request.json.get('description', '')

        # Optional status, if not provided keep original
        status_value = request.json.get('status', '')

        # If status is provided but is not one of the allowed options
        if status_value != '' and status_value not in ['OnGoing', 'NotStarted', 'Completed']:
            return get_server_response(status=0, msg="status must be from 'OnGoing','NotStarted','Completed'")

        # If all provided data is correct, go ahead and update required fields
        else:

            update_todo_item(todo_item, name, description, status_value)

        return get_server_response(status=1, msg="Todo item updated", data={'id': todo_item.Id,
                                                                            'user': todo_item.UserId,
                                                                            'name': todo_item.Name,
                                                                            'description': todo_item.Description,
                                                                            'status': todo_item.status})


@todosController.delete("/todos:<int:id>")
@jwt_required()
def DeleteItem(id):
    # Get id of current user
    current_user = get_jwt_identity()

    # Query todo item based on current user id and item id
    todo_item = get_todo_item_by_id(current_user , id)

    # If no item found corresponding to the current user and providid item id
    if not todo_item:
        return get_server_response(status=0, msg="Item not found")

    # If item is found
    else:
        delete_todo_item_from_db(todo_item)
        return  get_server_response(status=1, msg="Item Deleted Successfully")
