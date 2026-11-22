"use strict";

// Token guardado solamente en memoria.
// Se pierde al recargar la página por seguridad.
let token = null;
let ultimaPrediccion = null;

// 1. ELEMENTOS DE LA PÁGINA

const $ = (id) => document.getElementById(id);

const loginSection = $("loginSection");
const dashboard = $("dashboard");
const logoutBtn = $("logoutBtn");

const loginForm = $("loginForm");
const predictionForm = $("predictionForm");

const predictBtn = $("predictBtn");
const explainBtn = $("explainBtn");


// 2. FORMATO DE MONEDA Y FECHAS

function formatoCLP(valor) {
  return new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
    maximumFractionDigits: 0
  }).format(valor);
}

function formatoFecha(valor) {
  const fecha = new Date(valor);

  if (Number.isNaN(fecha.getTime())) {
    return valor;
  }

  return fecha.toLocaleString("es-CL");
}

// 3. MENSAJES


function mostrarMensaje(id, mensaje, tipo = "") {
  const elemento = $(id);

  elemento.textContent = mensaje;
  elemento.className = `message ${tipo}`;
}

function limpiarMensaje(id) {
  mostrarMensaje(id, "");
}

// 4. PETICIONES AL BACKEND

async function solicitarAPI(ruta, opciones = {}) {
  const encabezados = {
    ...(opciones.headers || {})
  };

  if (opciones.body !== undefined) {
    encabezados["Content-Type"] = "application/json";
  }

  if (token) {
    encabezados.Authorization = `Bearer ${token}`;
  }

  let respuesta;

  try {
    respuesta = await fetch(ruta, {
      ...opciones,
      headers: encabezados,
      cache: "no-store"
    });
  } catch {
    throw new Error(
      "No se pudo conectar con el servidor. " +
      "Comprueba que FastAPI esté ejecutándose."
    );
  }

  let datos;

  try {
    datos = await respuesta.json();
  } catch {
    throw new Error(
      "El servidor devolvió una respuesta inválida."
    );
  }

  if (!respuesta.ok) {
    if (
      respuesta.status === 401 &&
      ruta !== "/api/login"
    ) {
      cerrarSesion();
    }

    let detalle = datos.detail;

    if (Array.isArray(detalle)) {
      detalle = detalle
        .map((error) => {
          const campo = error.loc?.join(" / ") || "Campo";
          return `${campo}: ${error.msg}`;
        })
        .join(". ");
    }

    throw new Error(
      typeof detalle === "string"
        ? detalle
        : "No se pudo completar la operación."
    );
  }

  return datos;
}

// 5. INICIAR SESIÓN

loginForm.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  limpiarMensaje("loginMessage");

  const boton = loginForm.querySelector(
    'button[type="submit"]'
  );

  boton.disabled = true;
  boton.textContent = "Verificando...";

  try {
    const datos = await solicitarAPI("/api/login", {
      method: "POST",
      body: JSON.stringify({
        usuario: $("username").value.trim(),
        contrasena: $("password").value
      })
    });

    token = datos.access_token;

    // Cargar opciones antes de mostrar el panel.
    await cargarFormulario();

    loginSection.classList.add("hidden");
    dashboard.classList.remove("hidden");
    logoutBtn.classList.remove("hidden");

    $("password").value = "";

    await cargarMetricas();

  } catch (error) {
    mostrarMensaje(
      "loginMessage",
      error.message,
      "error"
    );
  } finally {
    boton.disabled = false;
    boton.textContent = "Ingresar a la plataforma";
  }
});

// 6. CERRAR SESIÓN

function cerrarSesion() {
  token = null;
  ultimaPrediccion = null;

  dashboard.classList.add("hidden");
  loginSection.classList.remove("hidden");
  logoutBtn.classList.add("hidden");

  $("password").value = "";

  reiniciarResultados();
}

logoutBtn.addEventListener("click", cerrarSesion);

// 7. CARGAR COMUNAS Y TIPOS DE PROPIEDAD

function llenarSelect(id, opciones) {
  const select = $(id);

  // Eliminar opciones anteriores.
  select.replaceChildren();

  const inicial = document.createElement("option");
  inicial.value = "";
  inicial.textContent = "Selecciona una opción";
  inicial.disabled = true;
  inicial.selected = true;

  select.appendChild(inicial);

  for (const opcion of opciones) {
    const elemento = document.createElement("option");
    elemento.value = opcion;
    elemento.textContent = opcion;

    select.appendChild(elemento);
  }
}

async function cargarFormulario() {
  const datos = await solicitarAPI("/api/schema");

  if (
    !datos.comunas?.length ||
    !datos.property_types?.length ||
    !datos.room_types?.length
  ) {
    throw new Error(
      "El modelo no devolvió suficientes categorías. " +
      "Revisa el preprocesador entrenado."
    );
  }

  llenarSelect("comuna", datos.comunas);

  llenarSelect(
    "propertyType",
    datos.property_types
  );

  llenarSelect(
    "roomType",
    datos.room_types
  );
}

// 8. VALIDAR NÚMEROS ENTEROS

function leerEntero(id, minimo, maximo) {
  const elemento = $(id);
  const valor = Number(elemento.value);

  if (
    elemento.value.trim() === "" ||
    !Number.isInteger(valor) ||
    valor < minimo ||
    valor > maximo
  ) {
    throw new Error(
      `El campo "${elemento.previousElementSibling?.textContent?.trim() || id}" ` +
      `debe ser un número entero entre ${minimo} y ${maximo}.`
    );
  }

  return valor;
}

// 9. VALIDAR NÚMEROS DECIMALES

function leerDecimal(id, minimo, maximo) {
  const elemento = $(id);
  const valor = Number(elemento.value);

  if (
    elemento.value.trim() === "" ||
    !Number.isFinite(valor) ||
    valor < minimo ||
    valor > maximo
  ) {
    throw new Error(
      `El campo ${id} debe estar entre ` +
      `${minimo} y ${maximo}.`
    );
  }

  return valor;
}

// 10. RECOGER DATOS DEL FORMULARIO

function obtenerDatosPropiedad() {
  if (!predictionForm.reportValidity()) {
    throw new Error(
      "Completa correctamente los campos."
    );
  }

  return {
    comuna: $("comuna").value,

    property_type: $("propertyType").value,

    room_type: $("roomType").value,

    accommodates: leerEntero(
      "accommodates", 1, 40
    ),

    bedrooms: leerEntero(
      "bedrooms", 0, 30
    ),

    beds: leerEntero(
      "beds", 0, 80
    ),

    minimum_nights: leerEntero(
      "minimumNights", 1, 365
    ),

    number_of_reviews: leerEntero(
      "reviews", 0, 100000
    ),

    review_scores_rating: leerDecimal(
      "rating", 0, 5
    ),

    reviews_per_month: leerDecimal(
      "reviewsPerMonth", 0, 1000
    ),

    host_is_superhost: $("superhost").checked
  };
}

// 11. REALIZAR PREDICCIÓN

predictionForm.addEventListener(
  "submit",
  async (evento) => {
    evento.preventDefault();

    limpiarMensaje("predictionMessage");

    predictBtn.disabled = true;
    predictBtn.textContent = "Calculando...";

    explainBtn.disabled = true;

    $("explanationSection").classList.add(
      "hidden"
    );

    ultimaPrediccion = null;

    try {
      const propiedad = obtenerDatosPropiedad();

      const resultado = await solicitarAPI(
        "/api/predict",
        {
          method: "POST",
          body: JSON.stringify(propiedad)
        }
      );

      ultimaPrediccion = propiedad;

      $("estimatedPrice").textContent = formatoCLP(
        resultado.precio_estimado
      ).replace(/\s?CLP/, "").trim();

      $("predictionLatency").textContent =
        `${resultado.latencia_ms} ms`;

      $("resultDescription").textContent =
        `Estimación por noche para una propiedad ` +
        `en ${propiedad.comuna}, con ` +
        `${propiedad.bedrooms} dormitorio(s).`;

      explainBtn.disabled = false;

      mostrarMensaje(
        "predictionMessage",
        "Predicción generada correctamente.",
        "success"
      );

      await cargarMetricas();

    } catch (error) {
      mostrarMensaje(
        "predictionMessage",
        error.message,
        "error"
      );
    } finally {
      predictBtn.disabled = false;
      predictBtn.textContent =
        "Calcular precio estimado";
    }
  }
);

// 12. EXPLICAR PREDICCIÓN

explainBtn.addEventListener("click", async () => {
  if (!ultimaPrediccion) {
    return;
  }

  explainBtn.disabled = true;
  explainBtn.textContent = "Analizando...";

  try {
    const resultado = await solicitarAPI(
      "/api/explain",
      {
        method: "POST",
        body: JSON.stringify(ultimaPrediccion)
      }
    );

    $("originalPrice").textContent = formatoCLP(
      resultado.precio_original
    );

    $("modifiedPrice").textContent = formatoCLP(
      resultado.precio_modificado
    );

    $("priceDifference").textContent = formatoCLP(
      resultado.diferencia_clp
    );

    $("percentageDifference").textContent =
      resultado.variacion_porcentual === null
        ? "Variación no calculable"
        : `Variación: ${resultado.variacion_porcentual}%`;

    $("explanationText").textContent =
      resultado.interpretacion;

    $("explanationSection").classList.remove(
      "hidden"
    );

    $("explanationSection").scrollIntoView({
      behavior: "smooth",
      block: "nearest"
    });

  } catch (error) {
    mostrarMensaje(
      "predictionMessage",
      error.message,
      "error"
    );
  } finally {
    explainBtn.disabled = false;
    explainBtn.textContent =
      "Explicar predicción";
  }
});

// 13. CARGAR MÉTRICAS E HISTORIAL

async function cargarMetricas() {
  const datos = await solicitarAPI("/api/metrics");

  $("totalPredictions").textContent =
    datos.predicciones;

  $("averageLatency").textContent =
    datos.latencia_modelo_ms === null
      ? "—"
      : `${datos.latencia_modelo_ms} ms`;

  const tabla = $("historyBody");
  tabla.replaceChildren();

  if (!datos.historial.length) {
    const fila = document.createElement("tr");
    const celda = document.createElement("td");

    celda.colSpan = 4;
    celda.textContent =
      "Todavía no hay predicciones registradas.";

    fila.appendChild(celda);
    tabla.appendChild(fila);
    return;
  }

  for (const registro of datos.historial) {
    const fila = document.createElement("tr");

    const valores = [
      registro.id,
      formatoFecha(registro.fecha),
      formatoCLP(registro.precio),
      `${registro.latencia_ms} ms`
    ];

    for (const valor of valores) {
      const celda = document.createElement("td");
      celda.textContent = valor;
      fila.appendChild(celda);
    }

    tabla.appendChild(fila);
  }
}

$("refreshBtn").addEventListener(
  "click",
  async () => {
    try {
      await cargarMetricas();
    } catch (error) {
      mostrarMensaje(
        "predictionMessage",
        error.message,
        "error"
      );
    }
  }
);

// 14. CREAR RESPALDO

$("backupBtn").addEventListener(
  "click",
  async () => {
    const boton = $("backupBtn");

    boton.disabled = true;
    boton.textContent = "Creando respaldo...";

    limpiarMensaje("backupMessage");

    try {
      const resultado = await solicitarAPI(
        "/api/admin/backup",
        {
          method: "POST"
        }
      );

      mostrarMensaje(
        "backupMessage",
        `Respaldo creado: ${resultado.nombre}`,
        "success"
      );

    } catch (error) {
      mostrarMensaje(
        "backupMessage",
        error.message,
        "error"
      );
    } finally {
      boton.disabled = false;
      boton.textContent = "Crear respaldo";
    }
  }
);

// 15. RESTABLECER FORMULARIO

function reiniciarResultados() {
  $("estimatedPrice").textContent = "—";
  $("predictionLatency").textContent = "—";

  $("resultDescription").textContent =
    "Completa el formulario para generar " +
    "tu primera estimación.";

  $("explanationSection").classList.add(
    "hidden"
  );

  explainBtn.disabled = true;
}

$("resetBtn").addEventListener("click", () => {
  predictionForm.reset();

  // Dejar las categorías sin seleccionar.
  $("comuna").selectedIndex = 0;
  $("propertyType").selectedIndex = 0;
  $("roomType").selectedIndex = 0;

  ultimaPrediccion = null;

  reiniciarResultados();
  limpiarMensaje("predictionMessage");
});

