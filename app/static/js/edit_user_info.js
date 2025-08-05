
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
                if (editElem.classList.contains('is-invalid')){
                    clearFieldError(editElem);
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
            showToast("Se guardaron los cambios exitosamente", "success")
        } else {
            switch(response.error.type) {
                case "FormValidationError":
                    applyFieldErrors(content, response.error.data);
                    showToast(response.error.message + " Por favor, revisa los campos marcados.", "error");
                    break;
                case "LimitError":
                    showToast(response.error.message, "warning");
                    break;
                default:
                    showToast("No se pudo realizar los cambios. Intenta más tarde.", "error");
                }
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
            showToast("Por favor, guarda o cancela el elemento en edición antes de agregar uno nuevo.", "warning")
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
            showToast("Se creó el nuevo elemento exitosamente.", "success")
        } else {
            switch(response.error.type) {
                case "FormValidationError":
                    applyFieldErrors(content, response.error.data);
                    showToast(response.error.message + " Por favor, revisa los campos marcados.", "error");
                    break;
                case "LimitError":
                    showToast(response.error.message, "warning");
                    break;
                default:
                    showToast("No se pudo crear el nuevo elemento. Intenta más tarde.", "error");
                }
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
            showToast("Se eliminó el elemento exitosamente.", "success")
        } else {
            switch(response.error.type) {
                case "FormValidationError":
                    applyFieldErrors(content, response.error.data);
                    showToast(response.error.message + " Por favor, revisa los campos marcados.", "error");
                    break;
                case "LimitError":
                    showToast(response.error.message, "warning");
                    break;
                default:
                    showToast("No se pudo eliminar el elemento. Intenta más tarde.", "error");
                }
        }
    }

    function applyFieldErrors(container, fieldErrors) {
        const inputs = container.querySelectorAll("input, textarea, select");

        inputs.forEach(input => {
            const fieldName = input.name;
            const errorMessages = fieldErrors[fieldName];

            const feedback = input.nextElementSibling; // div que le sigue al input

            // limpieza del estado anterior
            input.classList.remove("is-invalid");
            input.removeAttribute("aria-invalid");

            if (!input.dataset.originalDescribedby) {
                input.dataset.originalDescribedby = input.getAttribute("aria-describedby") || "";
            }

            let originalDescribedby = input.dataset.originalDescribedby.trim();
            input.setAttribute("aria-describedby", originalDescribedby || "");


            if (feedback && feedback.classList.contains("invalid-feedback")) {
                feedback.textContent = "";
            }

            if (errorMessages && errorMessages.length > 0) {
                input.classList.add("is-invalid");
                input.setAttribute("aria-invalid", "true");

                if (feedback && feedback.classList.contains("invalid-feedback")) {
                    if (!feedback.id) {
                        feedback.id = `error-${fieldName}`;
                    }
                    feedback.textContent = errorMessages.join(" ");

                    let describedbyIds = originalDescribedby ? originalDescribedby.split(/\s+/) : [];
                    if (!describedbyIds.includes(feedback.id)) {
                        describedbyIds.push(feedback.id);
                    }
                    input.setAttribute("aria-describedby", describedbyIds.join(" "));
                }

                // listeners para limpiar error si el usuario edita
                const clearError = () => {
                    clearFieldError(input);
                };
                input.addEventListener("input", clearError);
                input.addEventListener("change", clearError);
            }
        });

        // enfocar primer campo con error
        const firstInvalid = container.querySelector(".is-invalid");
        if (firstInvalid) firstInvalid.focus();
    }

    function clearFieldError(input) {
        const feedback = input.nextElementSibling;

        input.classList.remove("is-invalid");
        input.removeAttribute("aria-invalid");
        
        const originalDescribedby = input.dataset.originalDescribedby.trim();
        if (originalDescribedby) {
            input.setAttribute("aria-describedby", originalDescribedby);
        } else {
            input.removeAttribute("aria-describedby");
        }

        if (feedback && feedback.classList.contains("invalid-feedback")) {
            feedback.textContent = "";
        }

        input.removeEventListener("input", clearFieldError);
        input.removeEventListener("change", clearFieldError);
    }
});