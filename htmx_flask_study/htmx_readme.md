

```markdown
# HTMX Attributes Guide
A comprehensive overview of HTMX attributes used in the Task Manager application.

## Core HTMX Attributes Used

### 1. hx-post
**Usage in Project:**
```html
<form hx-post="/tasks" hx-target="#task-list" class="d-flex">
    <input type="text" name="title" class="form-control me-2" placeholder="Enter task..." required>
    <button type="submit" class="btn btn-primary">Add</button>
</form>
```
**Purpose:**
- Sends a POST request to the specified URL
- Used for creating new tasks
- Triggers when the form is submitted

**Benefits:**
- Handles form submissions without page reload
- Maintains a smooth user experience
- Automatically sends form data to the server

### 2. hx-delete
**Usage in Project:**
```html
<button class="btn btn-danger btn-sm"
        hx-delete="/tasks/{{ task.id }}/delete"
        hx-target="#task-list">
    Delete
</button>
```
**Purpose:**
- Sends a DELETE request to remove a task
- Used for deleting existing tasks
- Triggers on button click

**Benefits:**
- Implements proper REST methods
- Handles deletion without page refresh
- Provides immediate visual feedback

### 3. hx-target
**Usage in Project:**
```html
<div id="task-list">
    {% include 'partials/task_list.html' %}
</div>
```
**Purpose:**
- Specifies where the response HTML should be inserted
- Used with other HTMX attributes to update specific parts of the page
- Can target any element with an ID

**Benefits:**
- Enables partial page updates
- Maintains page context
- Reduces unnecessary DOM updates

### 4. hx-trigger
**Usage Example (implicit in our checkbox):**
```html
<input type="checkbox" 
       hx-post="/tasks/{{ task.id }}/toggle"
       hx-target="#task-list"
       class="form-check-input me-2">
```
**Purpose:**
- Defines when the HTMX request should fire
- Default trigger varies by element type
- Can be customized for different events

**Benefits:**
- Provides flexible interaction options
- Enables intuitive user interactions
- Supports various event types

## Common Patterns in the Project

### Task Creation Pattern
```html
<!-- Add Task Form -->
<form hx-post="/tasks" hx-target="#task-list">
```
**Flow:**
1. User enters task title
2. Form submission triggers POST request
3. Server processes request
4. Response updates task list
5. No page reload required

### Task Toggle Pattern
```html
<!-- Task Toggle Checkbox -->
<input type="checkbox" 
       hx-post="/tasks/{{ task.id }}/toggle"
       hx-target="#task-list">
```
**Flow:**
1. User clicks checkbox
2. POST request sent to toggle endpoint
3. Server updates task status
4. Updated task list returned
5. DOM updates automatically

### Task Deletion Pattern
```html
<!-- Delete Task Button -->
<button hx-delete="/tasks/{{ task.id }}/delete"
        hx-target="#task-list">
```
**Flow:**
1. User clicks delete button
2. DELETE request sent
3. Server removes task
4. Updated task list returned
5. DOM reflects changes immediately

## Best Practices Demonstrated

### 1. Targeted Updates
- Using specific IDs for targets
- Updating only necessary components
- Maintaining page state

### 2. Semantic HTTP Methods
- POST for creation
- DELETE for removal
- Proper REST architecture

### 3. User Feedback
- Immediate visual updates
- No page flicker
- Smooth transitions

### 4. Progressive Enhancement
- Works without JavaScript
- Enhanced with HTMX
- Fallback support

## Additional HTMX Features (Not Used But Available)

### 1. hx-swap
```html
<div hx-swap="outerHTML">
```
- Controls how content is swapped
- Options: innerHTML, outerHTML, beforeend, afterend

### 2. hx-indicator
```html
<div hx-indicator="#loading">
```
- Shows loading states
- Useful for longer requests
- Improves user experience

### 3. hx-confirm
```html
<button hx-confirm="Are you sure?">
```
- Adds confirmation dialogs
- Prevents accidental actions
- Enhances user safety

## Resources
- [HTMX Official Documentation](https://htmx.org/docs/)
- [HTMX Examples](https://htmx.org/examples/)
- [HTMX Attributes Reference](https://htmx.org/attributes/)
```

This markdown document provides:
- Detailed explanation of HTMX attributes used
- Real code examples from the project
- Flow explanations
- Best practices
- Additional features for future enhancement
- Useful resources for further learning

Feel free to add this to your project documentation for better understanding and reference.
