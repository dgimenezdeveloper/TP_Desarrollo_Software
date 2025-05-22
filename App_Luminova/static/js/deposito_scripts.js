// App_Luminova/static/js/deposito_scripts.js

// Estas variables globales DEBEN ser definidas en la plantilla HTML (deposito.html)
// ANTES de que este script se cargue. Ejemplo en deposito.html:
// <script>
//     const URL_AGREGAR_CAT_INSUMO = "{% url 'App_LUMINOVA:agregar_categoria_insumo_ajax' %}";
//     // ... y todas las demás URLs y rutas estáticas ...
//     const STATIC_URL_PLACEHOLDER_ITEM = "{% static 'img/placeholder_item.png' %}";
// </script>

let currentTableModalCategoryId = null;
let currentTableModalCategoryName = null;
let currentTableModalItemType = null;

// Instancias de Modales (se inicializarán en DOMContentLoaded)
let itemsTableModalInstance = null;
let agregarInsumoModalInstance = null;
let editarInsumoModalInstance = null;
let agregarProductoModalInstance = null;
let editarProductoModalInstance = null;
let crearCategoriaInsumoModalInstance = null;
let crearCategoriaProductoModalInstance = null;

function mostrarTab(tipo) {
    const insumosContent = document.getElementById("insumos-content");
    const productosContent = document.getElementById("productos-content");
    const insumosTabButton = document.getElementById("insumos-tab");
    const productosTabButton = document.getElementById("productos-tab");

    if (insumosContent) insumosContent.style.display = (tipo === 'insumos') ? "flex" : "none";
    if (productosContent) productosContent.style.display = (tipo === 'productos') ? "flex" : "none";
    if (insumosTabButton) insumosTabButton.classList.toggle("active", tipo === 'insumos');
    if (productosTabButton) productosTabButton.classList.toggle("active", tipo === 'productos');
}

function getCsrfToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
}

function renderCategoryCard(categoriaData, itemType) {
    const containerId = itemType === 'insumo' ? 'insumo-categories-container' : 'producto-categories-container';
    const container = document.getElementById(containerId);
    if (!container) return;

    // Asegúrate que STATIC_URL_DEFAULT_CAT_INSUMO y STATIC_URL_DEFAULT_CAT_PRODUCTO estén definidas globalmente
    const defaultImage = itemType === 'insumo' ? (typeof STATIC_URL_DEFAULT_CAT_INSUMO !== 'undefined' ? STATIC_URL_DEFAULT_CAT_INSUMO : '') : (typeof STATIC_URL_DEFAULT_CAT_PRODUCTO !== 'undefined' ? STATIC_URL_DEFAULT_CAT_PRODUCTO : '');
    const imageUrl = categoriaData.imagen_url || defaultImage;
    const categoryId = categoriaData.categoria_id || categoriaData.id; // Ajustar según lo que devuelva el backend

    const cardHtml = `
        <div class="col">
            <div class="card shadow-sm h-100 category-card" data-category-id="${categoryId}" data-category-name="${categoriaData.nombre}" data-item-type="${itemType}">
                <a href="#" class="text-decoration-none text-dark d-flex flex-column h-100 open-category-modal">
                    <img src="${imageUrl}" class="card-img-top object-fit-contain" alt="Categoría ${categoriaData.nombre}" style="height: 120px;">
                    <div class="card-body d-flex flex-column justify-content-center">
                        <h5 class="card-title text-center">${categoriaData.nombre}</h5>
                    </div>
                </a>
            </div>
        </div>`;

    const noItemsMessage = container.querySelector('p.text-white.text-center');
    if (noItemsMessage) {
        container.innerHTML = ''; // Limpiar mensaje "No hay categorías"
    }
    container.insertAdjacentHTML('beforeend', cardHtml);

    // Re-vincular eventos a todas las tarjetas en este contenedor
    document.querySelectorAll(`#${containerId} .open-category-modal`).forEach(cardLink => {
        cardLink.removeEventListener('click', handleCategoryCardClick); // Evitar duplicados
        cardLink.addEventListener('click', handleCategoryCardClick);
    });
}

function populateItemsTable(items, itemType, categoriaNombre) {
    const tbody = document.getElementById('modal-items-tbody');
    const headerRow = document.getElementById('table-header-row');
    const modalCategoryTitleEl = document.getElementById('modalCategoryTitle');
    const itemTypeInModalTextEl = document.getElementById('itemTypeInModalText');

    if (tbody) tbody.innerHTML = '';
    if (headerRow) headerRow.innerHTML = '';
    if (modalCategoryTitleEl) modalCategoryTitleEl.textContent = categoriaNombre;
    if (itemTypeInModalTextEl) itemTypeInModalTextEl.textContent = itemType === 'insumo' ? 'Insumo' : 'Producto';

    const placeholderImg = typeof STATIC_URL_PLACEHOLDER_ITEM !== 'undefined' ? STATIC_URL_PLACEHOLDER_ITEM : '';

    if (itemType === 'insumo' && headerRow) {
        headerRow.innerHTML = `<th>ID</th><th>Imagen</th><th>Descripción</th><th>Fabricante</th><th>Precio U.</th><th>Stock</th><th>Acciones</th>`;
        if (tbody) {
            items.forEach(item => {
                const row = `<tr id="item-row-${itemType}-${item.id}">
                    <td>${item.id}</td>
                    <td><img src="${item.imagen_url || placeholderImg}" alt="${item.descripcion}" style="width: 50px; height: 50px; object-fit: cover;"></td>
                    <td>${item.descripcion}</td><td>${item.fabricante || '-'}</td><td>${item.precio_unitario}</td><td>${item.stock}</td>
                    <td>
                        <button class="btn btn-sm btn-info btn-edit-item" data-id="${item.id}" data-type="${itemType}"><i class="bi bi-pencil-fill"></i></button>
                        <button class="btn btn-sm btn-danger btn-delete-item" data-id="${item.id}" data-type="${itemType}"><i class="bi bi-trash-fill"></i></button>
                    </td></tr>`;
                tbody.insertAdjacentHTML('beforeend', row);
            });
        }
    } else if (itemType === 'producto' && headerRow) {
        headerRow.innerHTML = `<th>ID</th><th>Imagen</th><th>Descripción</th><th>Precio U.</th><th>Stock</th><th>Acciones</th>`;
        if (tbody) {
            items.forEach(item => {
                const row = `<tr id="item-row-${itemType}-${item.id}">
                    <td>${item.id}</td>
                    <td><img src="${item.imagen_url || placeholderImg}" alt="${item.descripcion}" style="width: 50px; height: 50px; object-fit: cover;"></td>
                    <td>${item.descripcion}</td><td>${item.precio_unitario}</td><td>${item.stock}</td>
                    <td>
                        <button class="btn btn-sm btn-info btn-edit-item" data-id="${item.id}" data-type="${itemType}"><i class="bi bi-pencil-fill"></i></button>
                        <button class="btn btn-sm btn-danger btn-delete-item" data-id="${item.id}" data-type="${itemType}"><i class="bi bi-trash-fill"></i></button>
                    </td></tr>`;
                tbody.insertAdjacentHTML('beforeend', row);
            });
        }
    }
    addTableButtonListeners();
}

function updateRowInTable(itemData, itemType) {
    const rowId = `item-row-${itemType}-${itemData.id}`;
    const rowElement = document.getElementById(rowId);
    if (!rowElement) return;

    let newRowContent = '';
    const placeholderImg = typeof STATIC_URL_PLACEHOLDER_ITEM !== 'undefined' ? STATIC_URL_PLACEHOLDER_ITEM : '';
    const imageUrl = itemData.imagen_url || placeholderImg;

    if (itemType === 'insumo') {
        newRowContent = `<td>${itemData.id}</td><td><img src="${imageUrl}" alt="${itemData.descripcion}" style="width: 50px; height: 50px; object-fit: cover;"></td><td>${itemData.descripcion}</td><td>${itemData.fabricante || '-'}</td><td>${itemData.precio_unitario}</td><td>${itemData.stock}</td><td><button class="btn btn-sm btn-info btn-edit-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-pencil-fill"></i></button> <button class="btn btn-sm btn-danger btn-delete-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-trash-fill"></i></button></td>`;
    } else if (itemType === 'producto') {
         newRowContent = `<td>${itemData.id}</td><td><img src="${imageUrl}" alt="${itemData.descripcion}" style="width: 50px; height: 50px; object-fit: cover;"></td><td>${itemData.descripcion}</td><td>${itemData.precio_unitario}</td><td>${itemData.stock}</td><td><button class="btn btn-sm btn-info btn-edit-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-pencil-fill"></i></button> <button class="btn btn-sm btn-danger btn-delete-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-trash-fill"></i></button></td>`;
    }
    rowElement.innerHTML = newRowContent;
    addTableButtonListeners();
}

function addRowToTable(itemData, itemType) {
    const tbody = document.getElementById('modal-items-tbody');
    if (!tbody) return;
    
    let newRowHtml = '';
    const placeholderImg = typeof STATIC_URL_PLACEHOLDER_ITEM !== 'undefined' ? STATIC_URL_PLACEHOLDER_ITEM : '';
    const imageUrl = itemData.imagen_url || placeholderImg;

    if (itemType === 'insumo') {
        newRowHtml = `<tr id="item-row-${itemType}-${itemData.id}"><td>${itemData.id}</td><td><img src="${imageUrl}" alt="${itemData.descripcion}" style="width: 50px; height: 50px; object-fit: cover;"></td><td>${itemData.descripcion}</td><td>${itemData.fabricante || '-'}</td><td>${itemData.precio_unitario}</td><td>${itemData.stock}</td><td><button class="btn btn-sm btn-info btn-edit-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-pencil-fill"></i></button> <button class="btn btn-sm btn-danger btn-delete-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-trash-fill"></i></button></td></tr>`;
    } else if (itemType === 'producto') {
         newRowHtml = `<tr id="item-row-${itemType}-${itemData.id}"><td>${itemData.id}</td><td><img src="${imageUrl}" alt="${itemData.descripcion}" style="width: 50px; height: 50px; object-fit: cover;"></td><td>${itemData.descripcion}</td><td>${itemData.precio_unitario}</td><td>${itemData.stock}</td><td><button class="btn btn-sm btn-info btn-edit-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-pencil-fill"></i></button> <button class="btn btn-sm btn-danger btn-delete-item" data-id="${itemData.id}" data-type="${itemType}"><i class="bi bi-trash-fill"></i></button></td></tr>`;
    }
    tbody.insertAdjacentHTML('beforeend', newRowHtml);
    
    const noItemsMsgEl = document.getElementById('modal-no-items-message');
    if (noItemsMsgEl) noItemsMsgEl.style.display = 'none';
    addTableButtonListeners();
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('modalItemsTable')) itemsTableModalInstance = new bootstrap.Modal(document.getElementById('modalItemsTable'));
    if (document.getElementById('modalAgregarInsumo')) agregarInsumoModalInstance = new bootstrap.Modal(document.getElementById('modalAgregarInsumo'));
    if (document.getElementById('modalEditarInsumo')) editarInsumoModalInstance = new bootstrap.Modal(document.getElementById('modalEditarInsumo'));
    if (document.getElementById('modalAgregarProducto')) agregarProductoModalInstance = new bootstrap.Modal(document.getElementById('modalAgregarProducto'));
    if (document.getElementById('modalEditarProducto')) editarProductoModalInstance = new bootstrap.Modal(document.getElementById('modalEditarProducto'));
    if (document.getElementById('modalCrearCategoriaInsumo')) crearCategoriaInsumoModalInstance = new bootstrap.Modal(document.getElementById('modalCrearCategoriaInsumo'));
    if (document.getElementById('modalCrearCategoriaProducto')) crearCategoriaProductoModalInstance = new bootstrap.Modal(document.getElementById('modalCrearCategoriaProducto'));

    const formCrearCatInsumo = document.getElementById('formCrearCategoriaInsumo');
    if (formCrearCatInsumo) {
        formCrearCatInsumo.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(URL_AGREGAR_CAT_INSUMO, { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCsrfToken() }})
            .then(response => response.json()).then(data => {
                if (data.success) {
                    alert('Categoría de insumo creada!');
                    renderCategoryCard(data, 'insumo'); // 'data' debe contener {categoria_id, nombre, imagen_url}
                    if (crearCategoriaInsumoModalInstance) crearCategoriaInsumoModalInstance.hide();
                    this.reset();
                } else { alert('Error al crear categoría de insumo: ' + JSON.stringify(data.errors)); }
            }).catch(err => console.error("Error fetch crear cat insumo:", err));
        });
    }

    const formCrearCatProd = document.getElementById('formCrearCategoriaProducto');
    if(formCrearCatProd) {
        formCrearCatProd.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(URL_AGREGAR_CAT_PRODUCTO, { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCsrfToken() }})
            .then(response => response.json()).then(data => {
                if (data.success) {
                    alert('Categoría de producto creada!');
                    renderCategoryCard(data, 'producto'); // 'data' debe contener {categoria_id, nombre, imagen_url}
                    if (crearCategoriaProductoModalInstance) crearCategoriaProductoModalInstance.hide();
                    this.reset();
                } else { alert('Error al crear categoría de producto: ' + JSON.stringify(data.errors)); }
            }).catch(err => console.error("Error fetch crear cat producto:", err));
        });
    }
    
    document.querySelectorAll('.open-category-modal').forEach(cardLink => {
        cardLink.addEventListener('click', handleCategoryCardClick);
    });

    const btnOpenAgregarItem = document.getElementById('btnOpenAgregarItemModal');
    if (btnOpenAgregarItem) {
        btnOpenAgregarItem.addEventListener('click', function() {
            var modalToOpenInstance, formId, displayNameElementId, hiddenIdElementId;

            if (currentTableModalItemType === 'insumo') {
                modalToOpenInstance = agregarInsumoModalInstance;
                formId = 'formAgregarInsumo';
                displayNameElementId = 'display_agregar_insumo_categoria_nombre';
                hiddenIdElementId = 'hidden_agregar_insumo_categoria_id';
            } else if (currentTableModalItemType === 'producto') {
                modalToOpenInstance = agregarProductoModalInstance;
                formId = 'formAgregarProducto';
                displayNameElementId = 'display_agregar_producto_categoria_nombre';
                hiddenIdElementId = 'hidden_agregar_producto_categoria_id';
            } else { return; }

            const form = document.getElementById(formId);
            if (form) form.reset();
            
            const displayElement = document.getElementById(displayNameElementId);
            if (displayElement) displayElement.textContent = currentTableModalCategoryName;
            
            const hiddenElement = document.getElementById(hiddenIdElementId);
            if (hiddenElement) hiddenElement.value = currentTableModalCategoryId;
            
            if(itemsTableModalInstance) itemsTableModalInstance.hide();
            if(modalToOpenInstance) modalToOpenInstance.show();
        });
    }

    const formAgregarInsumo = document.getElementById('formAgregarInsumo');
    if (formAgregarInsumo) {
        formAgregarInsumo.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(URL_AGREGAR_INSUMO, { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCsrfToken() }})
            .then(response => response.json()).then(data => {
                if (data.success) {
                    alert('Insumo agregado!');
                    if (agregarInsumoModalInstance) agregarInsumoModalInstance.hide();
                    this.reset();
                    if (itemsTableModalInstance && currentTableModalCategoryId == data.insumo.categoria_id_actual && currentTableModalItemType === 'insumo') {
                        fetchAndShowItemsForCategory(currentTableModalCategoryId, currentTableModalItemType, currentTableModalCategoryName);
                    }
                } else { alert('Error al agregar insumo: ' + JSON.stringify(data.errors)); }
            }).catch(err => console.error("Error fetch agregar insumo:", err));
        });
    }
    
    const formEditarInsumo = document.getElementById('formEditarInsumo');
    if (formEditarInsumo) {
        formEditarInsumo.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(URL_EDITAR_INSUMO, { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCsrfToken() }})
            .then(response => response.json()).then(data => {
                if (data.success) {
                    alert('Insumo editado!');
                    if(editarInsumoModalInstance) editarInsumoModalInstance.hide();
                    if (itemsTableModalInstance && currentTableModalCategoryId == data.insumo.categoria_id_actual && currentTableModalItemType === 'insumo') {
                       fetchAndShowItemsForCategory(currentTableModalCategoryId, currentTableModalItemType, currentTableModalCategoryName);
                    }
                } else { alert('Error al editar insumo: ' + JSON.stringify(data.errors));}
            }).catch(err => console.error("Error fetch editar insumo:", err));
        });
    }

    const formAgregarProducto = document.getElementById('formAgregarProducto');
    if (formAgregarProducto) {
        formAgregarProducto.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(URL_AGREGAR_PRODUCTO, { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCsrfToken() }})
            .then(response => response.json()).then(data => {
                if (data.success) {
                    alert('Producto terminado agregado!');
                    if(agregarProductoModalInstance) agregarProductoModalInstance.hide();
                    this.reset();
                    if (itemsTableModalInstance && currentTableModalCategoryId == data.producto.categoria_id_actual && currentTableModalItemType === 'producto') {
                       fetchAndShowItemsForCategory(currentTableModalCategoryId, currentTableModalItemType, currentTableModalCategoryName);
                    }
                } else { alert('Error al agregar producto: ' + JSON.stringify(data.errors)); }
            }).catch(err => console.error("Error fetch agregar producto:", err));
        });
    }
    
    const formEditarProducto = document.getElementById('formEditarProducto');
    if (formEditarProducto) {
        formEditarProducto.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(URL_EDITAR_PRODUCTO, { method: 'POST', body: formData, headers: { 'X-CSRFToken': getCsrfToken() }})
            .then(response => response.json()).then(data => {
                if (data.success) {
                    alert('Producto editado!');
                    if(editarProductoModalInstance) editarProductoModalInstance.hide();
                    if (itemsTableModalInstance && currentTableModalCategoryId == data.producto.categoria_id_actual && currentTableModalItemType === 'producto') {
                        fetchAndShowItemsForCategory(currentTableModalCategoryId, currentTableModalItemType, currentTableModalCategoryName);
                    }
                } else { alert('Error al editar producto: ' + JSON.stringify(data.errors)); }
            }).catch(err => console.error("Error fetch editar producto:", err));
        });
    }
    
    // Llamada inicial para bindeo de botones existentes
    document.querySelectorAll('.open-category-modal').forEach(cardLink => {
        cardLink.addEventListener('click', handleCategoryCardClick);
    });

}); // Fin DOMContentLoaded

function fetchAndShowItemsForCategory(categoryId, itemType, categoryName) {
    if(itemsTableModalInstance) itemsTableModalInstance.show();
    
    const loadingMsgEl = document.getElementById('modal-loading-message');
    const tbodyEl = document.getElementById('modal-items-tbody');
    const noItemsMsgEl = document.getElementById('modal-no-items-message');
    const errorMsgEl = document.getElementById('modal-error-message');

    if(loadingMsgEl) loadingMsgEl.style.display = 'block';
    if(tbodyEl) tbodyEl.innerHTML = '';
    if(noItemsMsgEl) noItemsMsgEl.style.display = 'none';
    if(errorMsgEl) errorMsgEl.style.display = 'none';

    fetch(`${URL_GET_ITEMS_POR_CATEGORIA}?categoria_id=${categoryId}&item_type=${itemType}`)
    .then(response => response.json())
    .then(data => {
        if(loadingMsgEl) loadingMsgEl.style.display = 'none';
        if (data.success) {
            if (data.items.length > 0) {
                populateItemsTable(data.items, itemType, categoryName);
            } else {
                const modalCatTitle = document.getElementById('modalCategoryTitle');
                const itemTypeInModalTxt = document.getElementById('itemTypeInModalText');
                if(modalCatTitle) modalCatTitle.textContent = categoryName;
                if(itemTypeInModalTxt) itemTypeInModalTxt.textContent = itemType === 'insumo' ? 'Insumo' : 'Producto';
                if(noItemsMsgEl) noItemsMsgEl.style.display = 'block';
                
                const headerRow = document.getElementById('table-header-row');
                if(headerRow) {
                    headerRow.innerHTML = ''; 
                    if (itemType === 'insumo') {
                        headerRow.innerHTML = `<th>ID</th><th>Imagen</th><th>Descripción</th><th>Fabricante</th><th>Precio U.</th><th>Stock</th><th>Acciones</th>`;
                    } else if (itemType === 'producto') {
                        headerRow.innerHTML = `<th>ID</th><th>Imagen</th><th>Descripción</th><th>Precio U.</th><th>Stock</th><th>Acciones</th>`;
                    }
                }
            }
        } else {
            if(errorMsgEl) errorMsgEl.style.display = 'block';
            console.error("Error fetching items:", data.error);
        }
    }).catch(error => {
        if(loadingMsgEl) loadingMsgEl.style.display = 'none';
        if(errorMsgEl) errorMsgEl.style.display = 'block';
        console.error('Error en la petición AJAX:', error);
    });
}

function handleCategoryCardClick(event) {
    event.preventDefault();
    const card = event.currentTarget.closest('.category-card');
    if (card) {
        currentTableModalCategoryId = card.dataset.categoryId;
        currentTableModalCategoryName = card.dataset.categoryName;
        currentTableModalItemType = card.dataset.itemType;
        fetchAndShowItemsForCategory(currentTableModalCategoryId, currentTableModalItemType, currentTableModalCategoryName);
    }
}

function addTableButtonListeners() {
    document.querySelectorAll('.btn-edit-item').forEach(button => {
        button.removeEventListener('click', handleEditItemClick);
        button.addEventListener('click', handleEditItemClick);
    });
    document.querySelectorAll('.btn-delete-item').forEach(button => {
        button.removeEventListener('click', handleDeleteItemClick);
        button.addEventListener('click', handleDeleteItemClick);
    });
}

function handleEditItemClick(event) {
    const button = event.currentTarget;
    const itemId = button.dataset.id;
    const itemType = button.dataset.type;

    let getDataUrl = '';
    let modalToOpenInstance;
    let formId = '';
    
    if (itemType === 'insumo') {
        getDataUrl = `${URL_GET_INSUMO_DATA}?id=${itemId}`;
        modalToOpenInstance = editarInsumoModalInstance;
        formId = 'formEditarInsumo';
    } else if (itemType === 'producto') {
        getDataUrl = `${URL_GET_PRODUCTO_DATA}?id=${itemId}`;
        modalToOpenInstance = editarProductoModalInstance;
        formId = 'formEditarProducto';
    } else { return; }

    fetch(getDataUrl)
    .then(response => response.json())
    .then(dataResponse => {
        if (dataResponse.success) {
            const itemData = itemType === 'insumo' ? dataResponse.insumo : dataResponse.producto;
            const form = document.getElementById(formId);
            if (!form) return;
            
            const idField = form.querySelector(`[name="id"]`);
            if (idField) idField.value = itemData.id;

            const descField = form.querySelector(`[name="descripcion"]`);
            if (descField) descField.value = itemData.descripcion;

            const categoriaSelect = form.querySelector(`[name="categoria"]`);
            if (categoriaSelect) categoriaSelect.value = itemData.categoria; // Asume que itemData.categoria es el ID
            
            const precioField = form.querySelector(`[name="precio_unitario"]`);
            if(precioField) precioField.value = itemData.precio_unitario;

            const stockField = form.querySelector(`[name="stock"]`);
            if(stockField) stockField.value = itemData.stock;

            if (itemType === 'insumo') {
                const fabField = form.querySelector(`[name="fabricante"]`);
                if(fabField) fabField.value = itemData.fabricante;
                const teField = form.querySelector(`[name="tiempo_entrega"]`);
                if(teField) teField.value = itemData.tiempo_entrega;
                const provField = form.querySelector(`[name="proveedor"]`);
                if(provField) provField.value = itemData.proveedor;
            }
            
            // const currentImageElement = form.querySelector(`img[id^="current_imagen_"]`);
            // if (currentImageElement) { /* Lógica para mostrar imagen actual si existe */ }
            const imageInput = form.querySelector('input[type="file"][name="imagen"]');
            if(imageInput) imageInput.value = ''; // Limpiar selector de archivo

            if(itemsTableModalInstance) itemsTableModalInstance.hide();
            if(modalToOpenInstance) modalToOpenInstance.show();
        } else {
            alert('Error al cargar datos para editar: ' + dataResponse.error);
        }
    }).catch(err => console.error("Error fetch editar item data:", err));
}

function handleDeleteItemClick(event) {
    const button = event.currentTarget;
    const itemId = button.dataset.id;
    const itemType = button.dataset.type;

    if (confirm(`¿Estás seguro de eliminar este ${itemType} (ID: ${itemId})?`)) {
        fetch(URL_ELIMINAR_ARTICULO, {
            method: 'POST',
            body: new URLSearchParams({ 'id': itemId, 'item_type': itemType, 'csrfmiddlewaretoken': getCsrfToken() }),
            headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': getCsrfToken() }
        })
        .then(response => response.json()).then(data => {
            if (data.success) {
                alert(`${itemType.charAt(0).toUpperCase() + itemType.slice(1)} eliminado!`);
                const rowToRemove = document.getElementById(`item-row-${itemType}-${itemId}`);
                if (rowToRemove) rowToRemove.remove();
                
                const tbodyEl = document.getElementById('modal-items-tbody');
                const noItemsMsgEl = document.getElementById('modal-no-items-message');
                if (tbodyEl && tbodyEl.children.length === 0 && noItemsMsgEl) {
                    noItemsMsgEl.style.display = 'block';
                }
            } else { alert('Error al eliminar: ' + data.error); }
        }).catch(err => console.error("Error fetch eliminar item:", err));
    }
}