document.addEventListener("DOMContentLoaded", function () {
  console.log("Script loaded!");
  const statusChoices = window.kanbanData.statusChoices;
  const kanbanData = window.kanbanData.kanbanData;
  const kanbanBoard = document.getElementById("kanban-board");

  statusChoices.forEach(choice => {
      console.log(choice)
      const column = document.createElement("div");
      column.classList.add("col");
      column.innerHTML = `
          <div class="card">
              <div class="card-header">${choice}</div>
              <div class="card-body" id="${choice.toLowerCase().replace(/\s+/g, '-')}-column">
                  <!-- Lead cards will be dynamically added here -->
              </div>
          </div>
      `;
      kanbanBoard.appendChild(column);

      const columnId = `${choice.toLowerCase().replace(/\s+/g, '-')}-column`;
      const columnBody = document.getElementById(columnId);
      if (columnBody) {
          kanbanData[choice].forEach(leadData => {
              const card = document.createElement("div");
              card.classList.add("card");
              card.innerHTML = `
                  <div class="card-body">
                      <h5 class="card-title">${leadData.first_name} ${leadData.last_name}</h5>
                      <p class="card-text">Sector: ${leadData.sector}</p>
                      <!-- Add more lead details as needed -->
                  </div>
              `;
              columnBody.appendChild(card);
          });
      }
  });
});
