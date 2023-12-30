// Get the columns and cards
let columns = document.querySelectorAll('.column');
let cards = document.querySelectorAll('.kanban-lead-card');

// Add drag events to the cards
cards.forEach(card => {
    card.addEventListener('dragstart', dragStart);
});

// Add drag events to the columns
columns.forEach(column => {
    column.addEventListener('dragover', dragOver);
    column.addEventListener('drop', drop);
});

// Function to store the dragged card
let draggedCard = null;

function dragStart(event) {
    draggedCard = event.target;
    event.dataTransfer.setData('text/plain', ''); // Necessary for Firefox to allow dragging
}

function dragOver(event) {
  // Check if the element being dragged over is not the .card-header
  if (!event.target.classList.contains('card-header')) {
      event.preventDefault();
  }
}



function drop(event) {
  event.preventDefault();

  // Find the nearest .card-body element by traversing up the DOM
  let targetElement = event.target;
  while (targetElement && !targetElement.classList.contains('card-body')) {
      targetElement = targetElement.parentNode;
  }

  // If a .card-body is found, proceed with the drop logic
  if (targetElement) {
      // Get the id of the target column (which should be the parent .col element)
      let new_status = targetElement.parentNode.id;
      console.log(new_status);

      // Append the dragged card to the .card-body directly
      targetElement.appendChild(draggedCard);

      // Get the lead id
      let lead_id = draggedCard.id;

      // Send the AJAX request with CSRF token
      fetch('/update_lead/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': getCookie('csrftoken'),
          },
          body: `lead_id=${lead_id}&new_status=${new_status}`,
      })
      .then(response => response.json())
      .then(data => {
          console.log('Lead status updated successfully:', data);

          // Log the lead status after the update
          fetch(`/get_lead_status/${lead_id}/`)
              .then(response => response.json())
              .then(data => console.log('Lead status after update:', data))
              .catch(error => console.error('Error fetching lead status:', error));
      })
      .catch(error => {
          console.error('Error updating lead status:', error);
      });

      draggedCard = null;
  }
}


// Function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
