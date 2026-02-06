# 🛡️ Protocolo de Soberanía Técnica (Git-Ops)

Este documento es el manual de vuelo para asegurar el código en la nube.

## 🚦 El Semáforo (Estado)
Comando: `git status`
* **Para qué sirve:** Muestra qué archivos modificaste.
* **Alerta:** Si ves letras rojas, es que hay cambios sin guardar en la "bolsa".

## 📦 La Bolsa (Preparación)
Comando: `git add .`
* **Para qué sirve:** Mete TODOS los cambios (archivos nuevos y modificados) en la bolsa de envío.
* **Clave:** No olvidar el punto `.` final. Significa "todo".

## 🔒 El Sello (Compromiso)
Comando: `git commit -m "mensaje explicativo"`
* **Para qué sirve:** Cierra la bolsa y le pone una etiqueta oficial.
* **Ejemplo:** `git commit -m "feat: agregue nueva metrica al dashboard"`
* **Efecto:** Crea un punto de restauración en la historia.

## 🚀 El Despegue (Nube)
Comando: `git push origin main`
* **Para qué sirve:** Sube los cambios guardados a GitHub.
* **Resultado:** Actualiza el repositorio remoto y asegura el código fuera de la PC.

---
**Recordatorio del Director Técnico:**
Si hay duda, ejecutar `git status` antes de nada.