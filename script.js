let editandoID = null;

    function limpiar() {
      document.getElementById("nombre").value = "";
      document.getElementById("dni").value = "";
      document.getElementById("fecha").value = "";
      document.getElementById("diagnostico").value = "";
      document.getElementById("tratamiento").value = "";
      document.getElementById("obra_social").value = "";
      editandoID = null;
    }

    function guardar() {
        const data = {
            nombre: document.getElementById("nombre").value,
            dni: document.getElementById("dni").value,
            fecha: document.getElementById("fecha").value,
            diagnostico: document.getElementById("diagnostico").value,
            tratamiento: document.getElementById("tratamiento").value,
            obra_social: document.getElementById("obra_social").value
            };

      const url = editandoID ? `http://127.0.0.1:5000/historia/${editandoID}` : "http://127.0.0.1:5000/historia";
      const metodo = editandoID ? "PUT" : "POST";

      fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      }).then(() => {
        limpiar();
        listar();
      });
    }

    function listar() {
      const filtro = document.getElementById("filtro").value;
      fetch(`http://127.0.0.1:5000/historias?filtro=${filtro}`)
        .then(res => res.json())
        .then(data => {
          const tbody = document.querySelector("#tabla tbody");
          tbody.innerHTML = "";
          data.forEach(([id, nombre, dni, fecha, diag, trat,obrso]) => {
            tbody.innerHTML += `
              <tr>
                <td>${id}</td>
                <td>${nombre}</td>
                <td>${dni}</td>
                <td>${fecha}</td>
                <td>${diag}</td>
                <td>${trat}</td>
                <td>${obrso}</td>
                <td>
                  <button onclick='cargarEditar(${id}, "${nombre}", "${dni}", "${fecha}", "${diag}", "${trat}", "${obrso}")'>Editar</button>
                  <button onclick='eliminar(${id})'>Eliminar</button>
                </td>
              </tr>`;
          });
        });
    }

    function cargarEditar(id, nombre, dni, fecha, diag, trat, obrso) {
      document.getElementById("nombre").value = nombre;
      document.getElementById("dni").value = dni;
      document.getElementById("fecha").value = fecha;
      document.getElementById("diagnostico").value = diag;
      document.getElementById("tratamiento").value = trat;
      document.getElementById("obra_social").value = obrso;
      editandoID = id;
    }

    function eliminar(id) {
      fetch(`http://127.0.0.1:5000/historia/${id}`, { method: "DELETE" })
        .then(() => listar());
    }

    listar();