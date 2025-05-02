describe('Task in detail mode', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
    let taskid // task id
    let todoid // todo id
    let taskObject // task object
    let todoData // todo object
    // let todoData // todo object
    
    before(function () {
        // create a fabricated user from a fixture
        cy.fixture('user.json')
        .then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((userResponse) => {
                uid = userResponse.body._id.$oid
                name = user.firstName + ' ' + user.lastName
                email = user.email
            })

            // create a fabricated task from a fixture
            cy.fixture('task.json')
            .then((task) => {
                taskObject = task
                task.userid = uid
                // task.todos = JSON.stringify(task.todos)
                let taskData = new URLSearchParams();
                for (const key in task) {
                    taskData.append(key, task[key]);
                }

                taskData = taskData.toString()

                console.log("taskData", taskData)
                cy.log("taskData", taskData)

                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/tasks/create',
                    json: true,
                    body: taskData,
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                }).then((taskResponse) => {
                    cy.log("taskResponse", taskResponse)
                    console.log("taskResponse", taskResponse)
                    taskid = taskResponse.body[taskResponse.body.length - 1]._id.$oid
                    cy.log("taskid", taskid)
                })
            })
        })
    })

    beforeEach(function () {
        // enter the main main page
        cy.visit('http://localhost:3000')
        // login
        // detect a div which contains "Email Address", find the input and type (in a declarative way)
        cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type(email)
        // submit the form on this page
        cy.get('form')
        .submit()
        // assert that the user is now logged in
        cy.get('h1')
        .should('contain.text', 'Your tasks, ' + name)
        // assert that the task at least ones task is present
        cy.get('div.container')
        .find('div.container-element')
        .should('have.length.at.least', 2)
        // click on the created task
        // cy.contains('div.container-element', 'Test task 1')
        // .find('a').click()
        cy.contains('Test task').click()
        // assert that the task is now opened and in detail view mode
        cy.get('div.popup-inner')
        .should('exist')
    })

    it('creating a new todo item', () => {
        // enter the description of the todo item in the input field
        cy.fixture('todo.json')
        .then((todo) => {
            todoData = todo
            // enter description
            cy.get('form.inline-form')
            .find('input[type=text]')
            .scrollIntoView()
            .type(todo.description)
            // todoData = todo

            // click on the "Add" button
            cy.contains('input[type=submit]', 'Add').click()
            // assert that the created todo item is now present at the bottom of the list
            cy.get('ul.todo-list')
            .find('li.todo-item')
            .last()
            .contains(todo.description)
            .should('exist')
        })
    })

    it('creating a new todo item with empty description', () => {
        // make sure description is empty
        cy.get('form.inline-form')
        .find('input[type=text]')
        .should('have.value', '')

        // assert that the "Add" button is disabled
        cy.get('input[type=submit][value="Add"]')
        .should('be.disabled')
    })

    it('check a todo item as done', () => {
        // check the first todo item
        cy.get('ul.todo-list')
        .find('li.todo-item')
        .first()
        .find('span.checker')
        .should('have.class', 'unchecked')
        .click()
        // assert that the todo item is now marked as done
        cy.get('ul.todo-list')
        .find('li.todo-item')
        .first()
        .find('span.checker')
        .should('have.class', 'checked')
    })

    it('check a todo item as not done', () => {
        // unchcheck the first todo item
        cy.get('ul.todo-list')
        .find('li.todo-item')
        .first()
        .find('span.checker')
        .should('have.class', 'checked')
        .click()
        // assert that the todo item is now marked as not done
        cy.get('ul.todo-list')
        .find('li.todo-item')
        .first()
        .find('span.checker')
        .should('have.class', 'unchecked')
    })

    it('delete a todo item', () => {
        // delete the first todo item
        cy.get('ul.todo-list')
        .contains('li.todo-item', taskObject.todos)
        .contains('✖')
        .click()
        // assert that the todo item is now deleted
        cy.get('ul.todo-list')
        .contains('li.todo-item', taskObject.todos)
        .should('not.exist')
    })


    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
        // clean up by deleting all tasks for the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/tasks/byid/${taskid}`
            }).then((response) => {
            cy.log(response.body)
            })
        // // clean up by deleting the todo from the database
        // cy.request({
        //   method: 'DELETE',
        //   url: `http://localhost:5000/todos/${todoid}`
        // }).then((response) => {
        //   cy.log(response.body)
        // })
    })
})
