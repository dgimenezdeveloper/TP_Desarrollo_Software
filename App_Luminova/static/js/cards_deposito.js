// static/js/cards_deposito.js

document.addEventListener('DOMContentLoaded', function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Función de ayuda para crear el HTML de la tarjeta (USADO PARA RESULTADOS DE BÚSQUEDA)
    function createCardHtml(item, type) {
        const defaultInsumoImage = "/static/img/default_insumo.png";
        const defaultProductImage = "/static/img/default_product.png";

        const imageUrl = item.imagen_url ? item.imagen_url : (type === 'insumo' ? defaultInsumoImage : defaultProductImage);

        return `
            <div class="col">
                <div class="card shadow-sm h-100">
                    <img src="${imageUrl}" class="card-img-top object-fit-contain" alt="${item.descripcion}" style="height: 150px;">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${item.descripcion}</h5>
                        <p class="card-text"><strong>Categoría:</strong> ${item.categoria}</p>
                        ${type === 'insumo' ? `<p class="card-text"><strong>Fabricante:</strong> ${item.fabricante}</p>` : ''}
                        <p class="card-text"><strong>Precio:</strong> $${parseFloat(item.precio_unitario).toFixed(2)}</p>
                        ${type === 'insumo' ? `<p class="card-text"><strong>Tiempo de Entrega:</strong> ${item.tiempo_entrega} días</p>` : ''}
                        ${type === 'insumo' ? `<p class="card-text"><strong>Proveedor:</strong> ${item.proveedor}</p>` : ''}
                        <p class="card-text"><strong>Stock:</strong> ${item.stock}</p>
                        <div class="mt-auto d-flex justify-content-between">
                            <button class="btn btn-sm btn-info edit-btn" data-id="${item.id}" data-type="${type}" data-bs-toggle="modal" data-bs-target="#modalEditar${type === 'insumo' ? 'Insumo' : 'Producto'}">Editar</button>
                            <button class="btn btn-sm btn-danger delete-btn" data-id="${item.id}" data-type="${type}">Eliminar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Función para crear el HTML de la fila de la tabla (USADO PARA EL MODAL DE CATEGORÍAS)
    function createTableRowHtml(item, type) {
        // Establecer una URL de imagen por defecto si no existe
        const defaultInsumoImage = "/static/img/default_insumo.png";
        const defaultProductImage = "/static/img/default_product.png";
        const imageUrl = item.imagen_url ? item.imagen_url : (type === 'insumo' ? defaultInsumoImage : defaultProductImage);


        let rowHtml = `
            <tr>
        `;

        // Columna de Imagen para insumos
        if (type === 'insumo') {
            rowHtml += `
                <td><img src="${imageUrl}" alt="${item.descripcion}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;"></td>
            `;
        }

        rowHtml += `
                <td>${item.id}</td>
                <td>${item.descripcion}</td>
                <td>${item.categoria}</td>
        `;

        if (type === 'insumo') {
            rowHtml += `
                <td>${item.fabricante}</td>
                <td>$${parseFloat(item.precio_unitario).toFixed(2)}</td>
                <td>${item.tiempo_entrega} días</td>
                <td>${item.proveedor}</td>
            `;
        } else { // Producto
            rowHtml += `
                <td>$${parseFloat(item.precio_unitario).toFixed(2)}</td>
            `;
        }

        rowHtml += `
                <td>${item.stock}</td>
                <td>
                    <button class="btn btn-sm btn-info edit-btn" data-id="${item.id}" data-type="${type}" data-bs-toggle="modal" data-bs-target="#modalEditar${type === 'insumo' ? 'Insumo' : 'Producto'}">Editar</button>
                    <button class="btn btn-sm btn-danger delete-btn" data-id="${item.id}" data-type="${type}">Eliminar</button>
                </td>
            </tr>
        `;
        return rowHtml;
    }

    // Función para cargar ítems en la tabla del modal
    window.loadItemsInTable = async function(categoryName, itemType) {
        console.log(`[loadItemsInTable] Cargando ítems para categoría: ${categoryName}, tipo: ${itemType}`);
        const modalCategoryTitle = document.getElementById('modalCategoryTitle');
        const modalItemsTbody = document.getElementById('modal-items-tbody');
        const tableHeaderRow = document.getElementById('table-header-row');
        const loadingMessage = document.getElementById('modal-loading-message');
        const noItemsMessage = document.getElementById('modal-no-items-message');
        const errorMessage = document.getElementById('modal-error-message');

        // Limpiar y mostrar mensaje de carga
        modalCategoryTitle.textContent = categoryName;
        modalItemsTbody.innerHTML = '';
        tableHeaderRow.innerHTML = '';
        loadingMessage.style.display = 'block';
        noItemsMessage.style.display = 'none';
        errorMessage.style.display = 'none';

        // Definir encabezados de tabla según el tipo de ítem
        let headers = ``;
        if (itemType === 'insumo') {
            headers += `<th>Imagen</th>`; // Nueva columna de Imagen al inicio para insumos
        }
        headers += `<th>ID</th><th>Descripción</th><th>Categoría</th>`;
        if (itemType === 'insumo') {
            headers += `<th>Fabricante</th><th>Precio</th><th>Tiempo de Entrega</th><th>Proveedor</th>`;
        } else { // Producto
            headers += `<th>Precio</th>`;
        }
        headers += `<th>Stock</th><th>Acciones</th>`;
        tableHeaderRow.innerHTML = headers;

        const url = itemType === 'insumo' ?
            `/App_LUMINOVA/get-insumos-por-categoria/?categoria=${encodeURIComponent(categoryName)}` :
            `/App_LUMINOVA/get-productos-terminados/?categoria=${encodeURIComponent(categoryName)}`;

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log('[loadItemsInTable] Datos recibidos:', data);

            loadingMessage.style.display = 'none';
            if (data.success && (data.insumos || data.productos)) {
                const items = data.insumos || data.productos;
                if (items.length > 0) {
                    items.forEach(item => {
                        modalItemsTbody.innerHTML += createTableRowHtml(item, itemType);
                    });
                    attachCrudListeners(); // Re-adjuntar escuchadores después de cargar el contenido
                } else {
                    noItemsMessage.style.display = 'block';
                }
            } else {
                errorMessage.style.display = 'block';
                console.error('[loadItemsInTable] Error al cargar ítems:', data.error || 'Error desconocido');
            }
        } catch (error) {
            loadingMessage.style.display = 'none';
            errorMessage.style.display = 'block';
            console.error(`[loadItemsInTable] Error cargando ${itemType}s para categoría ${categoryName}:`, error);
        }
    };

    // Event listener para cuando se muestra el modal de ítems (modalItemsTable)
    const modalItemsTable = document.getElementById('modalItemsTable');
    if (modalItemsTable) {
        modalItemsTable.addEventListener('show.bs.modal', function (event) {
            console.log('[modalItemsTable] Modal de tabla mostrado.');
            const button = event.relatedTarget;
            const categoryName = button.getAttribute('data-category-name');
            const itemType = button.getAttribute('data-item-type');

            if (categoryName && itemType) {
                modalItemsTable.dataset.currentItemType = itemType;
                modalItemsTable.dataset.currentCategoryName = categoryName;
                console.log(`[modalItemsTable] Abriendo tabla para categoría: ${categoryName}, tipo: ${itemType}`);
                loadItemsInTable(categoryName, itemType);
            } else {
                console.error('[modalItemsTable] No se pudo obtener la categoría o el tipo de ítem del botón que abrió el modal.');
                document.getElementById('modal-error-message').style.display = 'block';
                document.getElementById('modal-loading-message').style.display = 'none';
            }
        });

        // Limpiar el contenido del modal cuando se cierra
        modalItemsTable.addEventListener('hidden.bs.modal', function () {
            console.log('[modalItemsTable] Modal de tabla oculto.');
            document.getElementById('modal-items-tbody').innerHTML = '';
            document.getElementById('table-header-row').innerHTML = '';
            document.getElementById('modalCategoryTitle').textContent = '';
            document.getElementById('modal-loading-message').style.display = 'none';
            document.getElementById('modal-no-items-message').style.display = 'none';
            document.getElementById('modal-error-message').style.display = 'none';
            delete modalItemsTable.dataset.currentItemType;
            delete modalItemsTable.dataset.currentCategoryName;
        });
    }

    // Función para cerrar un modal específico y limpiar el DOM/estado de Bootstrap
    function closeModal(modalId) {
        console.log(`[closeModal] Intentando cerrar modal: #${modalId}`);
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            let modalInstance = bootstrap.Modal.getInstance(modalElement);

            if (modalInstance) {
                modalInstance.hide();
                console.log(`[closeModal] Instancia de Bootstrap.Modal encontrada y hide() llamado para #${modalId}.`);
            } else {
                // Crear una instancia si no existe para intentar cerrar correctamente
                modalInstance = new bootstrap.Modal(modalElement);
                modalInstance.hide();
                console.log(`[closeModal] Instancia de Bootstrap.Modal creada y hide() llamado para #${modalId}.`);
            }

            // Limpieza agresiva del backdrop y la clase modal-open en el body
            setTimeout(() => {
                const backdrops = document.querySelectorAll('.modal-backdrop');
                backdrops.forEach(backdrop => {
                    console.log(`[closeModal] Removiendo backdrop:`, backdrop);
                    backdrop.remove();
                });
                
                if (document.body.classList.contains('modal-open')) {
                    document.body.classList.remove('modal-open');
                    console.log('[closeModal] Removida clase modal-open del body.');
                }
                if (document.body.style.overflow === 'hidden') {
                    document.body.style.overflow = '';
                    console.log('[closeModal] Restaurado overflow del body.');
                }
                // Asegurarse de que el modal en sí esté oculto si la animación falla
                if (modalElement.classList.contains('show')) {
                    modalElement.classList.remove('show');
                    modalElement.setAttribute('aria-hidden', 'true');
                    modalElement.style.display = 'none';
                    console.log(`[closeModal] Forzado ocultamiento visual de #${modalId}.`);
                }
            }, 300);
        } else {
            console.warn(`[closeModal] Intento de cerrar modal inexistente: #${modalId}`);
        }
    }

    // Funciones para recargar el contenido del modal de tabla después de un CRUD
    function reloadModalTableAfterCrud(itemType, categoryName) {
        console.log(`[reloadModalTableAfterCrud] Verificando si recargar tabla para ${categoryName} (${itemType}).`);
        const modalItemsTableEl = document.getElementById('modalItemsTable');
        // Verificar si el modal de la tabla de ítems está abierto y si es la categoría/tipo que se está mostrando
        if (modalItemsTableEl && modalItemsTableEl.classList.contains('show') &&
            modalItemsTableEl.dataset.currentItemType === itemType &&
            modalItemsTableEl.dataset.currentCategoryName === categoryName) {
            
            console.log(`[reloadModalTableAfterCrud] Condiciones cumplidas, recargando modal de tabla para ${categoryName} (${itemType}).`);
            loadItemsInTable(categoryName, itemType);
        } else {
            console.log(`[reloadModalTableAfterCrud] Modal de tabla para ${categoryName} (${itemType}) no abierto o no es la categoría actual. No se recarga automáticamente.`);
        }
    }


    // Envío del formulario para Agregar Insumo
    const formAgregarInsumo = document.getElementById('formAgregarInsumo');
    if (formAgregarInsumo) {
        formAgregarInsumo.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('[formAgregarInsumo] Formulario de agregar insumo enviado.');
            const formData = new FormData(formAgregarInsumo);

            try {
                const response = await fetch('/App_LUMINOVA/agregar-insumo/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    body: formData
                });
                const data = await response.json();
                console.log('[formAgregarInsumo] Respuesta del servidor:', data);

                if (data.success) {
                    alert('¡Insumo agregado con éxito!');
                    closeModal('modalAgregarInsumo');
                    console.log('[formAgregarInsumo] Insumo agregado con éxito, recargando página...');
                    location.reload(); // Recargar toda la página para que las categorías se actualicen
                } else {
                    alert('Error al agregar insumo: ' + JSON.stringify(data.errors || data.error));
                }
            } catch (error) {
                console.error('[formAgregarInsumo] Error en la petición:', error);
                alert('Error de red al agregar insumo.');
            }
        });
    }

    // Envío del formulario para Agregar Producto Terminado
    const formAgregarProducto = document.getElementById('formAgregarProducto');
    if (formAgregarProducto) {
        formAgregarProducto.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('[formAgregarProducto] Formulario de agregar producto enviado.');
            const formData = new FormData(formAgregarProducto);

            try {
                const response = await fetch('/App_LUMINOVA/agregar-producto/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    body: formData
                });
                const data = await response.json();
                console.log('[formAgregarProducto] Respuesta del servidor:', data);

                if (data.success) {
                    alert('¡Producto terminado agregado con éxito!');
                    closeModal('modalAgregarProducto');
                    console.log('[formAgregarProducto] Producto agregado con éxito, recargando página...');
                    location.reload(); // Recargar toda la página para que las categorías se actualicen
                } else {
                    alert('Error al agregar producto: ' + JSON.stringify(data.errors || data.error));
                }
            } catch (error) {
                console.error('[formAgregarProducto] Error en la petición:', error);
                alert('Error de red al agregar producto terminado.');
            }
        });
    }

    // Adjuntar escuchadores para los botones de Editar y Eliminar
    function attachCrudListeners() {
        const editButtons = document.querySelectorAll('.edit-btn');
        const deleteButtons = document.querySelectorAll('.delete-btn');

        // Eliminar listeners existentes y adjuntar nuevos para evitar duplicados
        editButtons.forEach(button => {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);
            
            newButton.addEventListener('click', async function() {
                console.log('[edit-btn] Botón Editar clickeado.');
                const itemId = this.dataset.id;
                const itemType = this.dataset.type;

                closeModal('modalItemsTable'); // Cerrar el modal de la tabla de artículos

                try {
                    const url = itemType === 'insumo' ? 
                        `/App_LUMINOVA/get-insumo-data/?id=${itemId}` : 
                        `/App_LUMINOVA/get-producto-terminado-data/?id=${itemId}`;
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    console.log('[edit-btn] Datos del ítem para editar:', data);

                    if (data.success) {
                        const item = itemType === 'insumo' ? data.insumo : data.producto;
                        
                        if (itemType === 'insumo') {
                            document.getElementById('edit_insumo_id').value = item.id;
                            document.getElementById('edit_descripcion_insumo').value = item.descripcion;
                            document.getElementById('edit_categoria_insumo').value = item.categoria;
                            document.getElementById('edit_fabricante_insumo').value = item.fabricante;
                            document.getElementById('edit_precio_unitario_insumo').value = item.precio_unitario;
                            document.getElementById('edit_tiempo_entrega_insumo').value = item.tiempo_entrega;
                            document.getElementById('edit_proveedor_insumo').value = item.proveedor;
                            document.getElementById('edit_stock_insumo').value = item.stock;

                            const currentImage = document.getElementById('current_imagen_insumo');
                            if (item.imagen_url) {
                                currentImage.src = item.imagen_url;
                                currentImage.style.display = 'block';
                            } else {
                                currentImage.src = "/static/img/default_insumo.png"; // Asegurar imagen por defecto en edición
                                currentImage.style.display = 'block';
                            }

                            const formEditarInsumo = document.getElementById('formEditarInsumo');
                            if (formEditarInsumo) {
                                formEditarInsumo.dataset.originalCategory = item.categoria;
                            }
                            new bootstrap.Modal(document.getElementById('modalEditarInsumo')).show();
                            console.log('[edit-btn] Abriendo modalEditarInsumo.');
                        } else if (itemType === 'producto') {
                            document.getElementById('edit_producto_id').value = item.id;
                            document.getElementById('edit_descripcion_producto').value = item.descripcion;
                            document.getElementById('edit_categoria_producto').value = item.categoria;
                            document.getElementById('edit_precio_unitario_producto').value = item.precio_unitario;
                            document.getElementById('edit_stock_producto').value = item.stock;

                            const formEditarProducto = document.getElementById('formEditarProducto');
                            if (formEditarProducto) {
                                formEditarProducto.dataset.originalCategory = item.categoria;
                            }
                            new bootstrap.Modal(document.getElementById('modalEditarProducto')).show();
                            console.log('[edit-btn] Abriendo modalEditarProducto.');
                        }
                    } else {
                        alert('Error al cargar datos del ítem: ' + data.error);
                    }
                } catch (error) {
                    console.error('[edit-btn] Error al obtener datos del ítem:', error);
                    alert('Error de red al obtener datos del ítem.');
                }
            });
        });

        deleteButtons.forEach(button => {
            const newButton = button.cloneNode(true);
            button.parentNode.replaceChild(newButton, button);

            newButton.addEventListener('click', async function() {
                console.log('[delete-btn] Botón Eliminar clickeado.');
                const itemId = this.dataset.id;
                const itemType = this.dataset.type;
                
                const modalItemsTableEl = document.getElementById('modalItemsTable');
                let category = '';
                if (modalItemsTableEl && modalItemsTableEl.dataset.currentCategoryName) {
                    category = modalItemsTableEl.dataset.currentCategoryName;
                }

                if (confirm(`¿Estás seguro de que quieres eliminar este ${itemType === 'insumo' ? 'insumo' : 'producto terminado'}?`)) {
                    const formData = new FormData();
                    formData.append('id', itemId);
                    formData.append('model_type', itemType);

                    try {
                        const response = await fetch('/App_LUMINOVA/eliminar-articulo/', {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken,
                            },
                            body: new URLSearchParams(formData)
                        });
                        const data = await response.json();
                        console.log('[delete-btn] Respuesta del servidor al eliminar:', data);

                        if (data.success) {
                            alert(`${itemType === 'insumo' ? 'Insumo' : 'Producto terminado'} eliminado con éxito.`);
                            if (category) {
                                console.log(`[delete-btn] Recargando modal de tabla después de eliminar para categoría: ${category}.`);
                                reloadModalTableAfterCrud(itemType, category); 
                            } else {
                                console.log('[delete-btn] Artículo eliminado sin categoría activa, recargando página...');
                                location.reload();
                            }
                        } else {
                            alert('Error al eliminar: ' + (data.error || 'Error desconocido'));
                        }
                    } catch (error) {
                        console.error('[delete-btn] Error de red al eliminar:', error);
                        alert('Error de red al eliminar el artículo.');
                    }
                }
            });
        });
    }

    // Envío del formulario para Editar Insumo
    const formEditarInsumo = document.getElementById('formEditarInsumo');
    if (formEditarInsumo) {
        formEditarInsumo.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('[formEditarInsumo] Formulario de editar insumo enviado.');
            const formData = new FormData(formEditarInsumo);
            const originalCategory = formEditarInsumo.dataset.originalCategory;
            const newCategory = formData.get('categoria');

            try {
                const response = await fetch('/App_LUMINOVA/editar-insumo/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    body: formData
                });
                const data = await response.json();
                console.log('[formEditarInsumo] Respuesta del servidor:', data);

                if (data.success) {
                    alert('¡Insumo editado con éxito!');
                    closeModal('modalEditarInsumo');

                    if (originalCategory === newCategory) {
                        console.log('[formEditarInsumo] Categoría no cambió, intentando recargar modal de tabla.');
                        reloadModalTableAfterCrud('insumo', newCategory);
                    } else {
                        console.log('[formEditarInsumo] Categoría cambió, recargando página.');
                        location.reload(); 
                    }
                } else {
                    alert('Error al editar insumo: ' + JSON.stringify(data.errors || data.error));
                }
            } catch (error) {
                console.error('[formEditarInsumo] Error en la petición:', error);
                alert('Error de red al editar insumo.');
            }
        });
    }

    // Envío del formulario para Editar Producto
    const formEditarProducto = document.getElementById('formEditarProducto');
    if (formEditarProducto) {
        formEditarProducto.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('[formEditarProducto] Formulario de editar producto enviado.');
            const formData = new FormData(formEditarProducto);
            const originalCategory = formEditarProducto.dataset.originalCategory;
            const newCategory = formData.get('categoria');

            try {
                const response = await fetch('/App_LUMINOVA/editar-producto-terminado/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    },
                    body: formData
                });
                const data = await response.json();
                console.log('[formEditarProducto] Respuesta del servidor:', data);

                if (data.success) {
                    alert('¡Producto terminado editado con éxito!');
                    closeModal('modalEditarProducto');

                    if (originalCategory === newCategory) {
                        console.log('[formEditarProducto] Categoría no cambió, intentando recargar modal de tabla.');
                        reloadModalTableAfterCrud('producto', newCategory);
                    } else {
                        console.log('[formEditarProducto] Categoría cambió, recargando página.');
                        location.reload(); 
                    }
                } else {
                    alert('Error al editar producto: ' + JSON.stringify(data.errors || data.error));
                }
            } catch (error) {
                console.error('[formEditarProducto] Error en la petición:', error);
                alert('Error de red al editar producto terminado.');
            }
        });
    }

    // Funcionalidad de Búsqueda
    const btnBuscarArticulo = document.getElementById('btnBuscarArticulo');
    if (btnBuscarArticulo) {
        btnBuscarArticulo.addEventListener('click', async function() {
            console.log('[btnBuscarArticulo] Botón Buscar clickeado.');
            const searchQuery = document.getElementById('search_query').value.toLowerCase();
            const searchType = document.getElementById('search_type').value;
            const searchResultsDiv = document.getElementById('search_results');
            searchResultsDiv.innerHTML = '<p class="text-muted">Buscando...</p>';

            let fetchUrl;
            if (searchType === 'insumo') {
                fetchUrl = '/App_LUMINOVA/get-all-insumos/';
            } else if (searchType === 'producto') {
                fetchUrl = '/App_LUMINOVA/get-all-productos/';
            } else {
                searchResultsDiv.innerHTML = '<p>Tipo de búsqueda inválido.</p>';
                return;
            }

            try {
                const response = await fetch(fetchUrl);
                const data = await response.json();
                console.log('[btnBuscarArticulo] Resultados de búsqueda recibidos:', data);

                searchResultsDiv.innerHTML = '';
                if (data.success) {
                    const items = searchType === 'insumo' ? data.insumos : data.productos;
                    const filteredItems = items.filter(item =>
                        item.descripcion.toLowerCase().includes(searchQuery) ||
                        item.categoria.toLowerCase().includes(searchQuery) ||
                        (item.fabricante && item.fabricante.toLowerCase().includes(searchQuery)) ||
                        (item.proveedor && item.proveedor.toLowerCase().includes(searchQuery))
                    );
                    if (filteredItems.length > 0) {
                        filteredItems.forEach(item => {
                            searchResultsDiv.innerHTML += createCardHtml(item, searchType);
                        });
                    } else {
                        searchResultsDiv.innerHTML = '<p>No se encontraron artículos que coincidan con la búsqueda.</p>';
                    }
                    attachCrudListeners(); // Adjuntar escuchadores a los resultados de búsqueda
                } else {
                    searchResultsDiv.innerHTML = '<p>Error al buscar artículos.</p>';
                }
            } catch (error) {
                console.error('[btnBuscarArticulo] Error buscando artículos:', error);
                searchResultsDiv.innerHTML = '<p>Error de red al buscar artículos.</p>';
            }
        });
    }
});