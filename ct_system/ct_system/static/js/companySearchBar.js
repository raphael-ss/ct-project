const searchField=document.querySelector('#searchField');
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
const tbody = document.querySelector(".table-body");


searchField.addEventListener("keyup", (e)=>{
    const searchValue = e.target.value;
    tbody.innerHTML = "";
    if (searchValue.trim().length > 0){
        paginationContainer.style.display = "none";
        fetch("empresas/pesquisar-empresas", {
            body: JSON.stringify({searchText:searchValue}),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("data", data);

            appTable.style.display = "none";
            tableOutput.style.display = "block";

            if (data.length === 0){
                tableOutput.innerHTML = "Nenhum resultado encontrado :/"
            }else{
                data.forEach((item)=>{
                    tbody.innerHTML += 
                `
            <tr>
            <td><a href="${updateCompanyUrl.replace('PLACEHOLDER', item.id)}">${item.id}</a></td>
            <td>${item.company_name}</td>
            <td>${item.first_name} ${item.last_name}</td>
            <td>${item.cnpj}</td>
            <td>${item.field_of_action}</td>
            <td>${item.annual_revenue}</td>
            <td>${item.n_of_employees}</td>
            </tr>`
                });
            }
        });
    }else{
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        tableOutput.style.display = "none";
    }
});