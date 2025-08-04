
document.addEventListener("DOMContentLoaded", function () {
    const handlers = {
        "edit-btn": (id) => {
            toggleEditMode(id, true);
            updateEditModeData(id);
        },
        "cancel-btn": (id) => toggleEditMode(id, false),
        "save-btn": async (id) => await updateData(id),
        "delete-btn": (id) => toggleDeleteButtons(id, true),
        "cancel-del-btn": (id) => toggleDeleteButtons(id, false),
        "confirm-del-btn": (id) => {
            removeElement(id);
            toggleDeleteButtons(id, false);
        },
        "add-btn": (id, target) => {
            const templateId = target.dataset.template;
            addNewElement(id, templateId);
            toggleAddButtons(id, true);
        },
        "save-add-btn": async (id) => await createNewElement(id),
        "cancel-add-btn": (id) => {
            cancelNewElement(id);
            toggleAddButtons(id, false);
        }
    };
    
    document.addEventListener("click", async (event) => {
        const target = event.target;
        const targetId = target.dataset.target;

        for (const [className, handler] of Object.entries(handlers)) {
            if (target.classList.contains(className)) {
                await handler(targetId, target);
                break;
            }
        }
    });

    function toggleEditMode(targetId, editing) {
        const container = document.getElementById(targetId);
        if (!container) return;

        container.querySelectorAll(".view-mode").forEach(el => {
            el.classList.toggle("d-none", editing);
        });

        const editElems = container.querySelectorAll(".edit-mode")
        editElems.forEach(el => {
            el.classList.toggle("d-none", !editing);
        });

        if (editing && editElems.length > 0) {
            const firstEditable = editElems[0];
            firstEditable.focus();
        }

        toggleEditButtons(targetId, editing);
    }

    function updateViewModeData(targetId) {
        const container = document.getElementById(targetId);
        if (!container) return;

        const booleanMap = {
            "true": "SI",
            "false": "NO"
        };

        const inputs = container.querySelectorAll("input, textarea, select");
        inputs.forEach(input => {
            const viewElem = input.parentElement.querySelector(".view-mode");
            if (!viewElem) return;

            let value = input.value;

            if(input.tagName === "INPUT" && value.trim() === ""){
                value = "-";
            }

            viewElem.textContent = booleanMap[value] ?? value;
            
        });
    }

    function updateEditModeData(targetId) {
        const container = document.getElementById(targetId);
        if (!container) return;

        const booleanMap = {
            "SI": "true",
            "NO": "false"
        };

        const viewElems = container.querySelectorAll(".view-mode");
        viewElems.forEach(viewElem => {
            const editElem = viewElem.parentElement.querySelector(".edit-mode");
            const value = viewElem.textContent;
            if (editElem) {
                editElem.value = (booleanMap[value.trim()] ?? (
                    (value === "-" || value.trim() === "") ? "" : value)) || "";
                if (editElem.classList.contains('autosize')) {
                    editElem.style.height = '0px';
                    editElem.style.height = editElem.scrollHeight + 'px';
                }
            }
        });
    }

    function toggleEditButtons(targetId, editing) {
        const editButtons = document.querySelectorAll(`[data-target="${targetId}"][data-role="edit"]`);
        const deleteButton = document.querySelector(`button.delete-btn[data-target="${targetId}"]`);
        
        editButtons.forEach(btn => {
        if (btn.classList.contains('edit-btn')) {
            btn.classList.toggle('d-none', editing);
            if (!editing) {
                btn.focus();
            }
        } else {
            btn.classList.toggle('d-none', !editing);
        }
        });
        
        if (deleteButton) {
            deleteButton.classList.toggle('d-none', editing);
        }
    }

    function toggleDeleteButtons(targetId, deleting) {
        const deleteButtons = document.querySelectorAll(`[data-target="${targetId}"][data-role="delete"]`);
        const editButton = document.querySelector(`button.edit-btn[data-target="${targetId}"]`);
        
        deleteButtons.forEach(btn => {
        if (btn.classList.contains('delete-btn')) {
            btn.classList.toggle('d-none', deleting);
            if (!deleting) {
                btn.focus();
            }
        } else {
            btn.classList.toggle('d-none', !deleting);
        }
        });
        
        if (editButton) {
            editButton.classList.toggle('d-none', deleting);
        }
    }

    function toggleAddButtons(targetId, adding){
        const addButtons = document.querySelectorAll(`[data-target="${targetId}"][data-role="add"]`);

        addButtons.forEach(btn => {
        if (btn.classList.contains('add-btn')) {
            btn.classList.toggle('d-none', adding);
            if (!adding) {
                btn.focus();
            }
        } else {
            btn.classList.toggle('d-none', !adding);
        }
        });
    }

    async function updateData(targetId){
        const content = document.getElementById(targetId);
        const dataToSend = {};
        const urlMap = {
            user: '/usuario/actualizar',
            contact: '/usuario/contacto/actualizar',
            medication: '/usuario/medicamento/actualizar',
        };

        const type = content.dataset.type; // contact, user or medication

        if(type !== "user"){
            dataToSend["id"] = Number(content.dataset.elementId);
        }

        const inputs = content.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
                    const fieldName = input.name;
                    dataToSend[fieldName] = input.value;
                });
        
        const payload = {[type]: dataToSend};
        const response = await postToEndpoint(urlMap[type], payload);

        if (response.success) {
            updateViewModeData(targetId)
            toggleEditMode(targetId, false)
            alert("Se guardaron los cambios exitosamente")
        } else {
            alert(response.error?.message || "Ocurrió un error inesperado.");
        }
    }

    async function postToEndpoint(url, payload){
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload),
            });

            const data = await response.json();

            return data;

        } catch (error) {
            return {
                success: false,
                error: {
                    message: 'No se pudo conectar con el servidor.',
                    type: 'NetworkError',
                    data: error
                }
            };
        }
    }

    function addNewElement(targetId,templateId) {
        const container = document.getElementById(targetId);
        const template = document.getElementById(templateId);
        
        if (container.querySelector('.list-item.editing')){
            alert("Por favor, guarda o cancela el elemento en edición antes de agregar uno nuevo.");
            return;
        }

        const clone = template.content.cloneNode(true);

        const currentElements = container.querySelectorAll('.list-item');
        if (currentElements.length === 0) {
            const hrInClone = clone.querySelector('hr');
            if (hrInClone) hrInClone.remove();
        }

        container.appendChild(clone);

        const newElementContent = container.querySelector(".list-item.editing .item-content");
        toggleEditMode(newElementContent.id, true);
    }

    function cancelNewElement(targetId){
        const container = document.getElementById(targetId);
        const editingElement = container.querySelector(".list-item.editing")

        if (editingElement){
            editingElement.remove();
            }
    }

    async function createNewElement(targetId){
        const container = document.getElementById(targetId); // contenedor del listado de elementos
        const editingElementContent = container.querySelector(".list-item.editing .item-content");
        const dataToSend = {};
        const urlMap = {
            contact: '/usuario/contacto/crear',
            medication: '/usuario/medicamento/crear',
        };

        const elemType = editingElementContent.dataset.type; // contact or medication

        const inputs = editingElementContent.querySelectorAll('input');
        inputs.forEach(input => {
            const fieldName = input.name;
            dataToSend[fieldName] = input.value.trim();
        });

        const payload = (elemType === "contact")? { 
            type: editingElementContent.dataset.contactType, 
            [elemType]: dataToSend } : { [elemType]: dataToSend };

        const response = await postToEndpoint(urlMap[elemType], payload);

        if (response.success) {
            updateViewModeData(editingElementContent.id)

            toggleAddButtons(targetId, false);
            
            const elementId = response.data[elemType].id;
            editingElementContent.setAttribute('data-element-id', elementId);

            if(elemType === "contact"){
                editingElementContent.removeAttribute('data-contact-type');
            }

            toggleEditMode(editingElementContent.id, false); 

            const currentElements = container.querySelectorAll('.list-item');
            let editingElement = container.querySelector('.list-item.editing');
            const newIndex = currentElements.length;
            editingElement.setAttribute('data-index', newIndex);
            updateIndex(editingElement, newIndex);

            editingElement = container.querySelector('.list-item.editing');
            editingElement.classList.remove('editing');
            const editBtns = editingElement.querySelector('.edit-btns');
            if (editBtns) {
                editBtns.classList.remove('d-none');
            }  
            
            alert("Se creó el nuevo elemento exitosamente")
        } else {
            alert(response.error?.message || "Ocurrió un error inesperado.");
        }
    }

    function updateIndex(element, newIndex) {
        const type = element.dataset.elem;
        const elemId = element.querySelector('.item-content')?.dataset.elementId;

        const title = element.querySelector('h5');
        if (title) {
            const titlesMap = {
            acompañante: "Acompañante",
            profesional: "Profesional",
            medicacion: "Medicación"
            };

            const baseText = titlesMap[type] || type;
            title.textContent = `${baseText} ${newIndex}:`;
        }

        let html = element.outerHTML;
        
        html = html.replace(/_X/g, `_${elemId}`);

        element.outerHTML = html;
    }

    async function removeElement(targetId) {
        const elemContainer = document.getElementById(targetId);
        const dataToSend = {};
        const urlMap = {
            contact: '/usuario/contacto/borrar',
            medication: '/usuario/medicamento/borrar',
        };

        const type = elemContainer.dataset.type; // contact or medication

        dataToSend["id"] = Number(elemContainer.dataset.elementId);

        const payload = { 
            [type]: dataToSend};

        const response = await postToEndpoint(urlMap[type], payload);

        if (response.success) {
            const itemListDeleted = elemContainer.closest('.list-item');
            
            if (!itemListDeleted) return;
            
            const listContainer = elemContainer.closest('.list-container')

            itemListDeleted.remove();

            const remainingItems = listContainer.querySelectorAll('.list-item');

            remainingItems.forEach((item, index) => {
                const correctIndex = index + 1;
                const actualIndex = item.dataset.index;

                if (correctIndex === actualIndex) return;

                if (index === 0) {
                    item.querySelector('hr')?.remove();
                }
                
                updateIndex(item, correctIndex);
            });

            alert("Se eliminó elemento exitosamente")
        } else {
            alert(response.error?.message || "Ocurrió un error inesperado.");
        }
    }
});