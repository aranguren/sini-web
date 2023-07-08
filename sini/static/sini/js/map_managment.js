function onEachFeatureWarning(feature, layer) {

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
    var boton_asignar = `<span data-bs-toggle="modal" data-bs-target="#executeModal">
        <button class="btn btn-link text-primary text-gradient px-0 mb-0 executebutton mx-2"
            id="asignar"
            data-bs-toggle="tooltip"
            data-bs-placement="top" title="Asignar a incidencia más cercana"
            value="${feature.properties.id}">
            <i class="fas fa-search-location fa-3x" aria-hidden="true"></i>
        </button>
    </span>`
    var boton_archivar = `<span data-bs-toggle="modal" data-bs-target="#deletePeriodoModal">
        <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
            id="eliminarVariable"
            data-bs-toggle="tooltip"
            data-bs-placement="top" title="Archivar"
            value="${feature.properties.id}">
            <i class="fa fa-archive fa-3x" aria-hidden="true"></i>
        </button>
        </span>`


  var popupContent = `<h6>${feature.properties.name}</h6>
    <p>${feature.properties.description}</p>
    <strong>Acciones</strong><br>
    <div class="row">
    <div class="col-12">`

    if(feature.properties.status=='creado'){
      popupContent+=boton_crear;
      popupContent+=boton_asignar;
  
    } 
    popupContent+=boton_archivar;
    
    popupContent+=`</div>
                </div>`
  layer.bindPopup(popupContent)
  layer.bindTooltip(feature.properties.name, { permanent: false })
}
function onEachFeatureIncidence(feature, layer) {
  layer.bindPopup(feature.properties.name)
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
function clicked(e)
{   
    console.log("clickedo elemento")
    var id_crear = e.target.id
    var result = id_crear.substring(11);
    var selectedwarning = document.getElementById('selectedWarning')
    selectedwarning.value = result
    console.log(selectedwarning.value)
  //e.preventDefault();
   // if(!confirm('Seguro de que desea guardar los cambios?')) {
   //     e.preventDefault();
    //}
}

  

document.getElementById("crearIncidencia").addEventListener('click', function(e){
    //var valor = document.getElementById('selectedWarning').value;
    console.log('CREAR INCIDENCIA');
    //console.log(valor);
    //var id_aviso = document.getElementById('selectedWarning').value;
    var prioridad = $('#id_prioridad_crear').find(":selected").val();

    //feature_warnings._layers.push(marker)
    //feature_incidence.addLayer(marker);
    var avisoId = document.getElementById('selectedWarning').value
    
    var request = $.ajax({
        type: "GET",
        url: "/sini/avisos/crear-incidencia/"+avisoId+"/",
        data: {
            "prioridad": prioridad
        },
        success: function (response) {
            console.log(response)
            $("#crearIncidenciaModal").modal('hide');
            console.log(response);
            //$(location).attr('href', "{% url 'sini:warning_detail' warning.id %}");
            var geojsonFeature = response.incidenceFeature
            var toadd = L.geoJSON(geojsonFeature ,{pointToLayer:redIcon, onEachFeature:onEachFeatureIncidence})
            console.log("Adicionando")
            console.log(toadd)
            feature_incidence.addLayer(toadd);

            for (var key in feature_warnings._layers) {
              // check if the property/key is defined in the object itself, not in parent
             console.log("mostrando llaves");
             console.log(key);
             console.log(feature_warnings._layers[key].feature.id)
             if(feature_warnings._layers[key].feature.id==avisoId){
              var boton_archivar = `<span data-bs-toggle="modal" data-bs-target="#deletePeriodoModal">
                <button class="btn btn-link text-danger text-gradient px-0 mb-0 deletebin mx-2"
                    id="eliminarVariable"
                    data-bs-toggle="tooltip"
                    data-bs-placement="top" title="Archivar"
                    value="${response.warningFeature.properties.id}">
                    <i class="fa fa-archive fa-3x" aria-hidden="true"></i>
                </button>
                </span>`


                var popupContent = `<h6>${response.warningFeature.properties.name}!!</h6>
                  <p>${response.warningFeature.properties.description}</p>
                  <strong>Acciones</strong><br>
                  <div class="row">
                  <div class="col-12">`

             
                  popupContent+=boton_archivar;
                  
                  popupContent+=`</div>
                              </div>`
              feature_warnings._layers[key]._popup._content = popupContent
             }
          }
            map_copy.closePopup();
            
        },
        error: function (response, e) {
            console.log(response);
            
            $("#crearIncidenciaModal").modal('hide');

         

            $('#errorModal').modal('show');
             var errorspan = document.getElementById('errorspan');
            
            if (response.responseJSON.mensaje =='restricted'){
                 errorspan.textContent = response.responseJSON.error;
            }
            else{
              errorspan.textContent ='Ha ocurrido un error al asignar, Contacte al Administrador';
            }
            
            
        }
    });
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
    });  
  

/*
        var persons= new L.GeoJSON.AJAX("{% url 'riesgo:worker_locate_all' %}" ,{
            // pointToLayer: function(feature, latlng){
            //           return new L.CircleMarker(latlng, {
            //           radius: 5,
            //            pane:"Dibujo",
            //            color:'red'
            //        });
            //},
         

            onEachFeature:function(feature,layer){
                layer.bindPopup(feature.properties.name+' '+feature.properties.last_name1);
            }
        });
*/
