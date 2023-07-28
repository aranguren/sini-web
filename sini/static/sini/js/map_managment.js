function onEachFeatureWarning(feature, layer) {
  var boton_detalles = `<a target="_blank" href="/sini/avisos/detalles/${feature.properties.id}/"  data-bs-toggle="tooltip"
  data-bs-placement="top" title="Detalles"><i class="far fa-eye fa-3x me-2 mx-2" aria-hidden="true"></i></a>`

  var boton_crear = `<span data-bs-toggle="modal" data-bs-target="#crearIncidenciaModal">
        <button class="crearButton btn btn-link text-primary text-gradient px-0 mb-0 executebutton mx-2"
            id="eliminarVariable"
            onclick="clicked(event)"
            data-bs-toggle="tooltip"
            data-bs-placement="top" title="Crear incidencia"
            value="${feature.properties.id}">
            <i id="buttonicon_${feature.properties.id}" class="fa fa-plus fa-3x" aria-hidden="true"></i>
        </button>
    </span>`
  var boton_asignar = `<span data-bs-toggle="modal" data-bs-target="#asingModal">
        <button class="btn btn-link text-primary text-gradient px-0 mb-0 executebutton mx-2"
            id="asignar"
            onclick="clicked_assign_closest(event)"
            data-bs-toggle="tooltip"
            data-bs-placement="top" title="Asignar a incidencia más cercana"
            value="${feature.properties.id}">
            <i id="assignicon_${feature.properties.id}" class="fas fa-search-location fa-3x" aria-hidden="true"></i>
        </button>
    </span>`

  var boton_desechar = `<span data-bs-toggle="modal" data-bs-target="#DescartarAvisoModal">
    <button class="btn btn-link text-primary text-gradient px-0 mb-0 mx-2"
        id="asignar"
        onclick="clicked_toss(event)"
        data-bs-toggle="tooltip"
        data-bs-placement="top" title="Desechar aviso"
        value="${feature.properties.id}">
        <i id="tossbutton_${feature.properties.id}" class="fa fa-eraser fa-2x" aria-hidden="true"></i>
      </button>
  </span>`

  var boton_archivar = `<span data-bs-toggle="modal" data-bs-target="#archiveWarningModal">
        <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
            id="eliminarVariable"
            onclick="clicked_archive_warning(event)"
            data-bs-toggle="tooltip"
            data-bs-placement="top" title="Archivar"
            value="${feature.properties.id}">
            <i id="archivicon_${feature.properties.id}" class="fa fa-archive fa-3x" aria-hidden="true"></i>
        </button>
        </span>`
  tipos = {
    accidente_aereo: 'Accidente aéreo',
    accidente_transito: 'Accidente de tránsito',
    colapso_puente: 'Alerta por colapso de puente',
    arbol_caido: 'Árbo caído',
    asfixia_inmersion: 'Asfixia por inmersión',
    aumento_cauce: 'Aumento de cauce',
    aumento_caudal: 'Aumento  de caudal',
  }
  status_dict = {
    creado: 'Creado',
    asignado: 'Asignado',
    descartado: 'Descartado',
  }
  tipo = tipos[feature.properties.incidence_type]
  status_value = status_dict[feature.properties.status]
  descripcion_str = feature.properties.description
  if (descripcion_str.length>90) {
    description = descripcion_str.slice(0,90)
    
  }
  else{
    description = descripcion_str
  }
  
  var popupContent = `<h6>Aviso: ${feature.properties.name}</h6>
    <div class="row mb-1 ">
      <div class="col-5"><b>Tipo incidente:</b></div>
      <div class="col-7">${tipo}</div>
    </div>
    <div class="row mb-3 text-right">
      <div class="col-5"><b>Status:</b></div>
      <div class="col-7">${status_value}</div>
    </div>
    <strong>Descripción</strong><br>
    <p class="mt-1 mb-2">${description}</p>
    <strong>Acciones</strong><br>
    <div class="row">
    <div class="col-12">`

    popupContent +=  boton_detalles
  if (feature.properties.status == 'creado') {
    popupContent += boton_crear
    popupContent += boton_asignar
    popupContent += boton_desechar
  }
  popupContent += boton_archivar

  popupContent += `</div>
                </div>`
  layer.bindPopup(popupContent, { minWidth: 300 })
  layer.bindTooltip(feature.properties.name, { permanent: false })
}
function onEachFeatureIncidence(feature, layer) {


  var boton_detalles = `<a target="_blank" href="/sini/incidencias/detalles/${feature.properties.id}/"  data-bs-toggle="tooltip"
  data-bs-placement="top" title="Detalles"><i class="far fa-eye fa-3x me-2 mx-2" aria-hidden="true"></i></a>`

    var boton_finalizar = `<span data-bs-toggle="modal" data-bs-target="#FinalizeIncidenciaModal">
          <button class="finalizarButton btn btn-link text-primary text-gradient px-0 mb-0 executebutton mx-2"
              id="finalizar_${feature.properties.id}"
              onclick="clicked_finalize_incidence(event)"
              data-bs-toggle="tooltip"
              data-bs-placement="top" title="Finalizar incidencia"
              value="${feature.properties.id}">
              <i id="buttonfina_${feature.properties.id}" class="fa fa-check fa-3x" aria-hidden="true"></i>
          </button>
      </span>`

    var boton_archivar = `<span data-bs-toggle="modal" data-bs-target="#ArchivarIncidenciaModal">
          <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
              id="eliminarVariable"
              onclick="clicked_archive_incidence(event)"
              data-bs-toggle="tooltip"
              data-bs-placement="top" title="Archivar"
              value="${feature.properties.id}">
              <i id="archivicon_${feature.properties.id}" class="fa fa-archive fa-3x" aria-hidden="true"></i>
          </button>
          </span>`
    tipos = {
      accidente_aereo: 'Accidente aéreo',
      accidente_transito: 'Accidente de tránsito',
      colapso_puente: 'Alerta por colapso de puente',
      arbol_caido: 'Árbo caído',
      asfixia_inmersion: 'Asfixia por inmersión',
      aumento_cauce: 'Aumento de cauce',
      aumento_caudal: 'Aumento  de caudal',
    }
    status_dict = {
      creado: 'Creado',
      finalizado: 'Finalizado',
    }
    tipo = tipos[feature.properties.incidence_type]
    status_value = status_dict[feature.properties.status]
    descripcion_str = feature.properties.description
    if (descripcion_str.length>90) {
      description = descripcion_str.slice(0,90)
      
    }
    else{
      description = descripcion_str
    }
    
    var popupContent = `<h6>Incidencia: ${feature.properties.name}</h6>
      <div class="row mb-1 ">
        <div class="col-5"><b>Tipo incidente:</b></div>
        <div class="col-7">${tipo}</div>
      </div>
      <div class="row mb-3 text-right">
        <div class="col-5"><b>Status:</b></div>
        <div class="col-7">${status_value}</div>
      </div>
      <strong>Descripción</strong><br>
      <p class="mt-1 mb-2">${description}</p>
      <strong>Acciones</strong><br>
      <div class="row">
      <div class="col-12">`

    //if (feature.properties.status == 'creado') {
    //  popupContent += boton_crear
    //  popupContent += boton_asignar
    //}
    popupContent +=boton_detalles
    popupContent += boton_finalizar
    popupContent += boton_archivar


    popupContent += `</div>
                  </div>`
    layer.bindPopup(popupContent, { minWidth: 300 })
    layer.bindTooltip(feature.properties.name, { permanent: false })


}

function style(feature) {
  var redMarker = L.ExtraMarkers.icon({
    icon: 'fa-coffee',
    markerColor: 'red',
    shape: 'square',
    prefix: 'fa',
  })

  return {
    icon: redMarker,
  }
}
function redIcon(point, latlng) {
  //https://github.com/coryasilva/Leaflet.ExtraMarkers#icons
  var redMarker = L.ExtraMarkers.icon({
    icon: 'fa-warning',
    markerColor: 'red',
    shape: 'circle',
    prefix: 'fa',
  })
  return L.marker(latlng, { icon: redMarker })
}

function orangeIcon(point, latlng) {
  var redMarker = L.ExtraMarkers.icon({
    icon: 'fa-warning',
    markerColor: 'orange',
    shape: 'circle',
    prefix: 'fa',
  })
  return L.marker(latlng, { icon: redMarker })
}

function clicked_assign_closest(e) {
  console.log('clickedo elemento')
  var id_crear = e.target.id
  var result = id_crear.substring(11)
  var selectedwarning = document.getElementById('selectedWarning')
  selectedwarning.value = result
  console.log(selectedwarning.value)

}

function clicked(e) {
  console.log('clickedo elemento');
  console.log('ahora vamos a crear');
  var id_crear = e.target.id
  var result = id_crear.substring(11)
  var selectedwarning = document.getElementById('selectedWarning')
  selectedwarning.value = result
  console.log(selectedwarning.value)
  //e.preventDefault();
  // if(!confirm('Seguro de que desea guardar los cambios?')) {
  //     e.preventDefault();
  //}
}

function clicked_archive_warning(e) {
  console.log('clickedo elemento')
  var id_crear = e.target.id
  var result = id_crear.substring(11)
  var selectedwarning = document.getElementById('selectedWarning')
  selectedwarning.value = result
  console.log(selectedwarning.value)

}
function clicked_toss(e) {
  console.log('desechando elmento elemento')
  var id_crear = e.target.id
  var result = id_crear.substring(11)
  var selectedwarning = document.getElementById('selectedWarning')
  selectedwarning.value = result
  console.log(selectedwarning.value)

}



// clic functions for incidence

function clicked_finalize_incidence(e) {
  console.log('clickedo elemento a finalizar')
  var id_crear = e.target.id
  var result = id_crear.substring(11)
  var selectedIncidence = document.getElementById('selectedIncidence')
  selectedIncidence.value = result
  console.log(selectedIncidence.value)

}
function clicked_archive_incidence(e) {
  console.log('clickedo elemento a finalizar')
  var id_crear = e.target.id
  var result = id_crear.substring(11)
  var selectedIncidence = document.getElementById('selectedIncidence')
  selectedIncidence.value = result
  console.log(selectedIncidence.value)

}



// asignar incidencia
document
  .getElementById('asignarIncidencia')
  .addEventListener('click', function (e) {
    //var valor = document.getElementById('selectedWarning').value;
    console.log('Asignar INCIDENCIA')

    var avisoId = document.getElementById('selectedWarning').value

    var request = $.ajax({
      type: 'GET',
      url: '/sini/avisos/asignar-cercana/' + avisoId + '/',
      data: {},
      success: function (response) {
        console.log(response)

        //$(location).attr('href', "{% url 'sini:warning_detail' warning.id %}");
        var geojsonFeature = response.incidenceFeature
        /*
        for (var key in feature_warnings._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves')
          console.log(key)
          console.log(feature_warnings._layers[key].feature.id)
          if (feature_warnings._layers[key].feature.id == avisoId) {
            var boton_archivar = `<span data-bs-toggle="modal" data-bs-target="#archiveModal">
                <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
                    id="eliminarVariable"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top" title="Archivar"
                    value="${response.warningFeature.properties.id}">
                    <i id="archiveicon_${response.warningFeature.properties.id}" class="fa fa-archive fa-3x" aria-hidden="true"></i>
                </button>
                </span>`
            tipos = {
              'accidente_aereo': 'Accidente aéreo',
              'accidente_transito': 'Accidente de tránsito',
              'colapso_puente': 'Alerta por colapso de puente',
              'arbol_caido': 'Árbo caído',
              'asfixia_inmersion': 'Asfixia por inmersión',
              'aumento_cauce': 'Aumento de cauce',
              'aumento_caudal': 'Aumento  de caudal',
            }
            status_dict = {
              'creado': 'Creado',
              'asignado': 'Asignado',
              'descartado': 'Descartado',
            }
            tipo = tipos[response.warningFeature.properties.incidence_type]
            status_value =
              status_dict[response.warningFeature.properties.status]

            var popupContent = `<h6>Aviso: ${response.warningFeature.properties.name}</h6>
              <div class="row mb-1 ">
                <div class="col-5"><b>Tipo incidente:</b></div>
                <div class="col-7">${tipo}</div>
              </div>
              <div class="row mb-3 text-right">
                <div class="col-5"><b>Status:</b></div>
                <div class="col-7">${status_value}</div>
              </div>
              <strong>Descripción</strong><br>
              <p class="mt-1 mb-2">${response.warningFeature.properties.description}</p>
              <strong>Acciones</strong><br>
              <div class="row">
              <div class="col-12">`

            popupContent += boton_archivar

            popupContent += `</div>
                            </div>`
            feature_warnings._layers[key]._popup._content = popupContent
          }
        }
        */
        for (var key in feature_warnings._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves');
          console.log(key)
          console.log(feature_warnings._layers[key].feature.id)
          if (feature_warnings._layers[key].feature.id == avisoId) {
            console.log("Se va a ocultar")
            feature_warnings.removeLayer(parseInt(key))
          }
        }
        var id_row = '#row_warning_'+avisoId;
        datatableWarnings.row( id_row ).remove().draw();
        $('#asingModal').modal('hide')
        map_copy.closePopup()
        var successSpan = document.getElementById('successSpan')
        successSpan.textContent = response.incidenceFeature.properties.name
        $('#assignSuccessModal').modal('show')
      },
      error: function (response, e) {
        console.log(response)

        $('#asingModal').modal('hide')

        $('#errorModal').modal('show')
        var errorspan = document.getElementById('errorspan')

        if (response.responseJSON.mensaje == 'no_incidence') {
          errorspan.textContent = 'No existen incidencias para asignar'
        } else {
          errorspan.textContent =
            'Ha ocurrido un error al asignar, Contacte al Administrador'
        }
      },
    })
  })

document
  .getElementById('crearIncidencia')
  .addEventListener('click', function (e) {
    //var valor = document.getElementById('selectedWarning').value;
    console.log('CREAR INCIDENCIA')
    //console.log(valor);
    //var id_aviso = document.getElementById('selectedWarning').value;
    var prioridad = $('#id_prioridad_crear').find(':selected').val()

    //feature_warnings._layers.push(marker)
    //feature_incidence.addLayer(marker);
    var avisoId = document.getElementById('selectedWarning').value

    var request = $.ajax({
      type: 'GET',
      url: '/sini/avisos/crear-incidencia/' + avisoId + '/',
      data: {
        prioridad: prioridad,
      },
      success: function (response) {
        console.log(response)
        $('#crearIncidenciaModal').modal('hide')
        
        console.log(response)
        //$(location).attr('href', "{% url 'sini:warning_detail' warning.id %}");
        var geojsonFeature = response.incidenceFeature

        var toadd = L.geoJSON(geojsonFeature, {
          pointToLayer: redIcon,
          onEachFeature: onEachFeatureIncidence,
        })
        console.log('Adicionando')
        console.log(toadd)
        feature_incidence.addLayer(toadd)
        console.log('/*/*/*/*/*/*/*/*/*/*/*/')
        console.log(toadd)
        /*
        for (var key in feature_warnings._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves')
          console.log(key)
          console.log(feature_warnings._layers[key].feature.id)
          if (feature_warnings._layers[key].feature.id == avisoId) {
            var boton_archivar = `<span data-bs-toggle="modal" data-bs-target="#archiveWarningModal">
                  <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
                      id="eliminarVariable"
                      data-bs-toggle="tooltip"
                      data-bs-placement="top" title="Archivar"
                      value="${response.warningFeature.properties.id}">
                      <i id="archiveicon_${response.warningFeature.properties.id}" class="fa fa-archive fa-3x" aria-hidden="true"></i>
                  </button>
                  </span>`
            tipos = {
              accidente_aereo: 'Accidente aéreo',
              accidente_transito: 'Accidente de tránsito',
              colapso_puente: 'Alerta por colapso de puente',
              arbol_caido: 'Árbo caído',
              asfixia_inmersion: 'Asfixia por inmersión',
              aumento_cauce: 'Aumento de cauce',
              aumento_caudal: 'Aumento  de caudal',
            }
            status_dict = {
              creado: 'Creado',
              asignado: 'Asignado',
              descartado: 'Descartado',
            }
            tipo = tipos[response.warningFeature.properties.incidence_type]
            status_value =
              status_dict[response.warningFeature.properties.status]

            var popupContent = `<h6>Aviso: ${response.warningFeature.properties.name}</h6>
                <div class="row mb-1 ">
                  <div class="col-5"><b>Tipo incidente:</b></div>
                  <div class="col-7">${tipo}</div>
                </div>
                <div class="row mb-3 text-right">
                  <div class="col-5"><b>Status:</b></div>
                  <div class="col-7">${status_value}</div>
                </div>
                <strong>Descripción</strong><br>
                <p class="mt-1 mb-2">${response.warningFeature.properties.description}</p>
                <strong>Acciones</strong><br>
                <div class="row">
                <div class="col-12">`

            popupContent += boton_archivar

            popupContent += `</div>
                              </div>`
            feature_warnings._layers[key]._popup._content = popupContent
          }
        }
        map_copy.closePopup()
        */
        for (var key in feature_warnings._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves');
          console.log(key)
          console.log(feature_warnings._layers[key].feature.id)
          if (feature_warnings._layers[key].feature.id == avisoId) {
            console.log("Se va a archivar")
            feature_warnings.removeLayer(parseInt(key))
          }
        }

        var id_row = '#row_warning_'+avisoId;
        datatableWarnings.row( id_row ).remove().draw();
        // ADICIONANDO A LA TABLA
        tipos = {
          accidente_aereo: 'Accidente aéreo',
          accidente_transito: 'Accidente de tránsito',
          colapso_puente: 'Alerta por colapso de puente',
          arbol_caido: 'Árbo caído',
          asfixia_inmersion: 'Asfixia por inmersión',
          aumento_cauce: 'Aumento de cauce',
          aumento_caudal: 'Aumento  de caudal',
        }
        status_dict = {
          creado: 'Creado',
          finalizado: 'Finalizado',
        }
        tipo = tipos[geojsonFeature.properties.incidence_type]
        status_value = status_dict[geojsonFeature.properties.status]

        var new_row_html = `<tr id="row_incidence_${geojsonFeature.properties.id}">
                      <td>${geojsonFeature.properties.name}</td>
                      <td>${geojsonFeature.properties.id}</td>
                      <td>${tipo}</td>
                      <td>${status_value}</td>
                      <td>${geojsonFeature.properties.date}</td>
                      <td class="text-center">
                        <a target="_blank" href="/sini/incidencias/detalles/${geojsonFeature.properties.id}/"  data-bs-toggle="tooltip"
                        data-bs-placement="top" title="Detalles"><i class="far fa-eye mx-2" aria-hidden="true"></i></a>
                      
                        <span data-bs-toggle="modal" data-bs-target="#FinalizeIncidenciaModal">
                          <button class="finalizarButton btn btn-link text-primary text-gradient px-0 mb-0  mx-2"
                              id="finalizar_${geojsonFeature.properties.id}"
                              onclick="clicked_finalize_incidence(event)"
                              data-bs-toggle="tooltip"
                              data-bs-placement="top" title="Finalizar incidencia"
                              value="${geojsonFeature.properties.id}">
                              <i id="buttonfina_${geojsonFeature.properties.id}" class="fa fa-check" aria-hidden="true"></i>
                          </button>
                      </span>

                      <span data-bs-toggle="modal" data-bs-target="#ArchivarIncidenciaModal">
                        <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
                            id="eliminarVariable"
                            onclick="clicked_archive_incidence(event)"
                            data-bs-toggle="tooltip"
                            data-bs-placement="top" title="Archivar"
                            value="${geojsonFeature.properties.id}">
                            <i id="archivicon_${geojsonFeature.properties.id}" class="fa fa-archive" aria-hidden="true"></i>
                        </button>
                        </span>

                      </td>
                    </tr>`
        datatableIncidences.row.add($(new_row_html)).draw();

        map_copy.closePopup()
        var successTitlelabel = document.getElementById('successTitlelabel')
        var successSpanLabel = document.getElementById('successSpanLabel')
        successTitlelabel.textContent = "Incidencia creada"
        successSpanLabel.textContent = " Se ha creado con éxito la incidencia a partir del aviso seleccionado. El aviso se ocultará"
        $('#operationSuccessModal').modal('show')
        //$('#createdSuccessModal').modal('show')
      },
      error: function (response, e) {
        console.log(response)

        $('#crearIncidenciaModal').modal('hide')

        $('#errorModal').modal('show')
        var errorspan = document.getElementById('errorspan')

        if (response.responseJSON.mensaje == 'restricted') {
          errorspan.textContent = response.responseJSON.error
        } else {
          errorspan.textContent =
            'Ha ocurrido un error al crear, Contacte al Administrador'
        }
      },
    })
    /*

    var geojsonFeature = {
      "type": "Feature",
      "properties": {
          "name": "Coors Field",
          "description": "Baseball Stadium",
          "id": "2345-dwert-2345-sdfg"
      },
      "geometry": {
          "type": "Point",
          "coordinates": [-69.89232, 18.47186 ]
      }
    };

    var toadd = L.geoJSON(geojsonFeature ,{pointToLayer:redIcon, onEachFeature:onEachFeatureIncidence})
    console.log("Adicionando")
    console.log(toadd)
    feature_incidence.addLayer(toadd);
*/
  })


  document
  .getElementById('archivarAviso')
  .addEventListener('click', function (e) {
    //var valor = document.getElementById('selectedWarning').value;
    console.log('ARCHIVAR AVISO')
    //console.log(valor);
    //var id_aviso = document.getElementById('selectedWarning').value;

    //feature_warnings._layers.push(marker)
    //feature_incidence.addLayer(marker);
    var avisoId = document.getElementById('selectedWarning').value

    var request = $.ajax({
      type: 'GET',
      url: '/sini/avisos/archivar/' + avisoId + '/',
      data: {},
      success: function (response) {
        console.log(response)
        $('#archiveWarningModal').modal('hide')

        console.log(response)
        console.log('mostrando modal');
        for (var key in feature_warnings._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves');
          console.log(key)
          console.log(feature_warnings._layers[key].feature.id)
          if (feature_warnings._layers[key].feature.id == avisoId) {
            console.log("Se va a archivar")
            feature_warnings.removeLayer(parseInt(key))
          }
        }
        map_copy.closePopup()
       
        var id_row = '#row_warning_'+avisoId;
        datatableWarnings.row( id_row ).remove().draw();
    
        //var rows = table.rows('.priority');
        var successTitlelabel = document.getElementById('successTitlelabel')
        var successSpanLabel = document.getElementById('successSpanLabel')
        successTitlelabel.textContent = "Aviso archivado"
        successSpanLabel.textContent = "El aviso seleccionado ha sido archivado. Por lo tanto se ocultará del mapa"
        $('#operationSuccessModal').modal('show')
      },
      error: function (response, e) {
        console.log(response)

        $('#crearIncidenciaModal').modal('hide')

        $('#errorModal').modal('show')
        var errorspan = document.getElementById('errorspan')

        if (response.responseJSON.mensaje == 'restricted') {
          errorspan.textContent = response.responseJSON.error
        } else {
          errorspan.textContent =
            'Ha ocurrido un error al asignar, Contacte al Administrador'
        }
      },
    })

  })

  // Desechar aviso

  document
  .getElementById('desecharAviso')
  .addEventListener('click', function (e) {
    //var valor = document.getElementById('selectedWarning').value;
    console.log('ARCHIVAR AVISO')
    //console.log(valor);
    //var id_aviso = document.getElementById('selectedWarning').value;

    //feature_warnings._layers.push(marker)
    //feature_incidence.addLayer(marker);
    var avisoId = document.getElementById('selectedWarning').value

    var request = $.ajax({
      type: 'GET',
      url: '/sini/avisos/descartar/' + avisoId + '/',
      data: {},
      success: function (response) {
        console.log(response)
        $('#DescartarAvisoModal').modal('hide')

        console.log(response)
        console.log('mostrando modal');
        for (var key in feature_warnings._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves');
          console.log(key)
          console.log(feature_warnings._layers[key].feature.id)
          if (feature_warnings._layers[key].feature.id == avisoId) {
            console.log("Se va a archivar")
            feature_warnings.removeLayer(parseInt(key))
          }
        }
        var id_row = '#row_warning_'+avisoId;
        datatableWarnings.row( id_row ).remove().draw();
        map_copy.closePopup()
        var successTitlelabel = document.getElementById('successTitlelabel')
        var successSpanLabel = document.getElementById('successSpanLabel')
        successTitlelabel.textContent = "Aviso descartado"
        successSpanLabel.textContent = "El aviso seleccionado ha sido descartado. Por lo tanto se ocultará del mapa"
        $('#operationSuccessModal').modal('show')
      },
      error: function (response, e) {
        console.log(response)

        $('#crearIncidenciaModal').modal('hide')

        $('#errorModal').modal('show')
        var errorspan = document.getElementById('errorspan')

        if (response.responseJSON.mensaje == 'restricted') {
          errorspan.textContent = response.responseJSON.error
        } else {
          errorspan.textContent =
            'Ha ocurrido un error al asignar, Contacte al Administrador'
        }
      },
    })

  })

  // Finalizar Incidencia
  document
  .getElementById('finalizarIncidencia')
  .addEventListener('click', function (e) {
    //var valor = document.getElementById('selectedWarning').value;
    console.log('Finalizar Incidencia')
    //console.log(valor);
    //var id_aviso = document.getElementById('selectedWarning').value;

    //feature_warnings._layers.push(marker)
    //feature_incidence.addLayer(marker);
    var avisoId = document.getElementById('selectedIncidence').value

    var request = $.ajax({
      type: 'GET',
      url: '/sini/incidencias/finalizar/' + avisoId + '/',
      data: {},
      success: function (response) {
        console.log(response)
        $('#FinalizeIncidenciaModal').modal('hide')

        console.log(response)
        console.log("mostrando todas las capas")
        console.log(feature_incidence._layers)
        for (var key in feature_incidence._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log(key)
          //console.log(feature_incidence._layers[key].feature.id)
          console.log('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
          console.log('Mostrando propiedades')
          console.log(feature_incidence._layers[key])
          console.log(feature_incidence._layers[key].feature)
          if (feature_incidence._layers[key].feature.properties.id == avisoId) {
            console.log("Se va a finalizar")
            feature_incidence.removeLayer(parseInt(key))
            break;
          }
        }
        //var id_row = '#row_incidence_'+avisoId;
        var rowTodelete = datatableIncidences.row({incidenceId:avisoId})
        rowTodelete.remove().draw();
        map_copy.closePopup()
        var successTitlelabel = document.getElementById('successTitlelabel')
        var successSpanLabel = document.getElementById('successSpanLabel')
        successTitlelabel.textContent = "Incidencia finalizada"
        successSpanLabel.textContent = "La incidencia seleccionada ha sido finalizada. Por lo tanto se ocultará del mapa"
        $('#operationSuccessModal').modal('show')
      },
      error: function (response, e) {
        console.log(response)

        $('#crearIncidenciaModal').modal('hide')

        $('#errorModal').modal('show')
        var errorspan = document.getElementById('errorspan')

        if (response.responseJSON.mensaje == 'restricted') {
          errorspan.textContent = response.responseJSON.error
        } else {
          errorspan.textContent =
            'Ha ocurrido un error al asignar, Contacte al Administrador'
        }
      },
    })

  })

  // Archivar incidencia

  document
  .getElementById('archivarIncidencia')
  .addEventListener('click', function (e) {
    //var valor = document.getElementById('selectedWarning').value;
    console.log('ARCHIVAR AVISO')
    //console.log(valor);
    //var id_aviso = document.getElementById('selectedWarning').value;

    //feature_warnings._layers.push(marker)
    //feature_incidence.addLayer(marker);
    var avisoId = document.getElementById('selectedIncidence').value

    var request = $.ajax({
      type: 'GET',
      url: '/sini/incidencias/archivar-map/' + avisoId + '/',
      data: {},
      success: function (response) {
        console.log(response)
        $('#ArchivarIncidenciaModal').modal('hide')

        console.log(response)
        console.log('mostrando modal');
        for (var key in feature_incidence._layers) {
          // check if the property/key is defined in the object itself, not in parent
          console.log('mostrando llaves');
          console.log(key)
          console.log(feature_incidence._layers[key].feature.id)
          if (feature_incidence._layers[key].feature.id == avisoId) {
            console.log("Se va a archivar")
            feature_incidence.removeLayer(parseInt(key))
          }
        }
        //var id_row = '#row_incidence_'+avisoId;
        //datatableIncidences.row( id_row ).remove().draw();
        var rowTodelete = datatableIncidences.row({incidenceId:avisoId});
        rowTodelete.remove().draw();
        map_copy.closePopup()
        var successTitlelabel = document.getElementById('successTitlelabel')
        var successSpanLabel = document.getElementById('successSpanLabel')
        successTitlelabel.textContent = "Incidencia archivada"
        successSpanLabel.textContent = "La incidencia seleccionada ha sido archivada. Por lo tanto se ocultará del mapa"
        $('#operationSuccessModal').modal('show')
      },
      error: function (response, e) {
        console.log(response)

        $('#crearIncidenciaModal').modal('hide')

        $('#errorModal').modal('show')
        var errorspan = document.getElementById('errorspan')

        if (response.responseJSON.mensaje == 'restricted') {
          errorspan.textContent = response.responseJSON.error
        } else {
          errorspan.textContent =
            'Ha ocurrido un error al asignar, Contacte al Administrador'
        }
      },
    })

  })