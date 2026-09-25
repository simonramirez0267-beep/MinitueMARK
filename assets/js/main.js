// MinuteMark · landing
//
// Número de WhatsApp comercial, solo dígitos y con el indicativo 57 (ej.: '573001234567').
// Si queda vacío, los formularios solo muestran el mensaje de gracias, como hasta ahora.
// Si tiene número, al enviar se abre WhatsApp con los datos ya escritos para que lleguen a ustedes.
var MM_WHATSAPP = '';

function mmAbrirWhatsApp(lineas){
  if (!MM_WHATSAPP) return;
  var texto = lineas.filter(Boolean).join('\n');
  window.open('https://wa.me/' + MM_WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
}

(function(){
  // --- cuestionario "Aplica tu unidad" ---
  var formAplica = document.getElementById('form-aplica');
  var graciasAplica = document.getElementById('gracias-aplica');
  if (formAplica) {
    formAplica.addEventListener('submit', function(e){
      e.preventDefault();
      var requeridos = ['zona','aptos','cerca','contacto-aplica'];
      var faltan = requeridos.filter(function(id){
        return !document.getElementById(id).value.trim();
      });
      if (faltan.length){
        var primero = document.getElementById(faltan[0]);
        primero.style.borderColor = '#D64545';
        primero.setAttribute('aria-invalid','true');
        primero.focus();
        return;
      }
      var v = function(id){ return document.getElementById(id).value.trim(); };
      mmAbrirWhatsApp([
        'Hola, MinuteMark. Quiero saber si mi unidad aplica.',
        'Zona: ' + v('zona'),
        'Apartamentos: ' + v('aptos'),
        v('salida') && ('Compra más frecuente: ' + v('salida')),
        'Tienda cerca: ' + v('cerca'),
        'Contacto: ' + v('contacto-aplica')
      ]);
      formAplica.hidden = true;
      graciasAplica.hidden = false;
      graciasAplica.scrollIntoView({behavior:'smooth', block:'center'});
    });
    ['zona','aptos','salida','cerca','contacto-aplica'].forEach(function(id){
      var el = document.getElementById(id);
      if (el) el.addEventListener('input', function(){ this.style.borderColor = ''; this.removeAttribute('aria-invalid'); });
      if (el) el.addEventListener('change', function(){ this.style.borderColor = ''; this.removeAttribute('aria-invalid'); });
    });
  }

  // --- formulario en dos pasos ---
  var form = document.getElementById('formulario');
  var paso1 = document.getElementById('paso1');
  var paso2 = document.getElementById('paso2');
  var etiqueta = document.getElementById('etiqueta-paso');
  var b2 = document.getElementById('b2');
  var gracias = document.getElementById('gracias');
  var resumen = document.getElementById('resumen');
  var saludo = document.getElementById('saludo');

  document.getElementById('continuar').addEventListener('click', function(){
    var faltan = ['nombre','unidad','telefono'].filter(function(id){
      return !document.getElementById(id).value.trim();
    });
    if (faltan.length){
      var primero = document.getElementById(faltan[0]);
      primero.style.borderColor = '#D64545';
        primero.setAttribute('aria-invalid','true');
      primero.focus();
      return;
    }
    paso1.hidden = true;
    paso2.hidden = false;
    etiqueta.textContent = 'Paso 2 de 2';
    b2.classList.add('on');
    document.getElementById('rol').focus();
  });

  ['nombre','unidad','telefono'].forEach(function(id){
    document.getElementById(id).addEventListener('input', function(){ this.style.borderColor = ''; this.removeAttribute('aria-invalid'); });
  });

  function linea(etiquetaTexto, valor){
    var d = document.createElement('div');
    var s = document.createElement('span');
    s.textContent = etiquetaTexto + ': ';
    d.appendChild(s);
    d.appendChild(document.createTextNode(valor));
    return d;
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var datos = {
      nombre: document.getElementById('nombre').value.trim(),
      unidad: document.getElementById('unidad').value.trim(),
      telefono: document.getElementById('telefono').value.trim(),
      correo: document.getElementById('correo').value.trim(),
      rol: document.getElementById('rol').value,
      tamano: document.getElementById('tamano').value,
      momento: document.getElementById('momento').value
    };
    saludo.textContent = 'Gracias, ' + datos.nombre.split(' ')[0] + '.';
    resumen.textContent = '';
    resumen.appendChild(linea('Unidad', datos.unidad));
    resumen.appendChild(linea('Contacto', datos.telefono + (datos.correo ? ' · ' + datos.correo : '')));
    resumen.appendChild(linea('Rol', datos.rol));
    resumen.appendChild(linea('Tamaño', datos.tamano));
    resumen.appendChild(linea('Momento', datos.momento));

    mmAbrirWhatsApp([
      'Hola, MinuteMark. Quiero llevar MinuteMark a mi unidad.',
      'Nombre: ' + datos.nombre,
      'Unidad: ' + datos.unidad,
      'WhatsApp: ' + datos.telefono,
      datos.correo && ('Correo: ' + datos.correo),
      'Rol: ' + datos.rol,
      'Apartamentos: ' + datos.tamano,
      'Momento: ' + datos.momento
    ]);
    form.hidden = true;
    gracias.hidden = false;
    gracias.scrollIntoView({behavior:'smooth', block:'center'});
  });

  // --- scroll reveal micro-animación ---
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var candidatos = document.querySelectorAll('.sec');
    candidatos.forEach(function(el){ el.classList.add('aparece','pendiente'); });
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){
          e.target.classList.remove('pendiente');
          obs.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    candidatos.forEach(function(el){ obs.observe(el); });
  }

  // --- el botón flotante se retira cuando ya estás en el formulario o en el pie ---
  var flota = document.querySelector('.flota');
  if (flota && 'IntersectionObserver' in window) {
    var enVista = [];
    var obsFlota = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        var i = enVista.indexOf(e.target);
        if (e.isIntersecting && i < 0) enVista.push(e.target);
        if (!e.isIntersecting && i > -1) enVista.splice(i, 1);
      });
      flota.classList.toggle('oculto', enVista.length > 0);
    }, { threshold: 0 });
    [document.querySelector('#contacto .form-bloque'), document.querySelector('.pie')].forEach(function(el){ if (el) obsFlota.observe(el); });
  }

  document.getElementById('otra').addEventListener('click', function(){
    form.reset();
    form.hidden = false;
    gracias.hidden = true;
    paso1.hidden = false;
    paso2.hidden = true;
    etiqueta.textContent = 'Paso 1 de 2';
    b2.classList.remove('on');
    document.getElementById('nombre').focus();
  });
})();
