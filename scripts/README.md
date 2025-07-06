## 📁 Estructura de archivos

```
Give-What-You-No-Longer-Use/
├── scripts/
│   ├── sync-old-repo.sh
│   └── README.md
└── abjes.md
```

---

## 📦 `scripts/sync-old-repo.sh`

```bash
#!/bin/bash

# 📦 Script de sincronización manual entre entornos Git
# Autor: Jesús Abregú
# Fecha: 5 de julio 2025

OLD_PATH="$HOME/Give-OLD"
CURRENT_PATH="$HOME/Give-What-You-No-Longer-Use"

echo "🔁 Iniciando sincronización desde $OLD_PATH a $CURRENT_PATH ..."
echo "🧼 Excluyendo .git para evitar conflictos de historial"

rsync -av --exclude='.git' "$OLD_PATH/" "$CURRENT_PATH/"

echo "✅ Sincronización completada."

cd "$CURRENT_PATH" || exit

echo "🔍 Verificando estado del repositorio..."
git status

read -p "¿Deseás agregar y commitear los cambios? (s/n): " RESP
if [[ "$RESP" =~ ^[sS](i)?$ ]]; then
    git add .
    git commit -m "Merge manual desde entorno Give-OLD: sincronización de archivos clave"
    git push origin abjes/setup-entorno-inicial
    echo "🚀 Cambios subidos con éxito."
else
    echo "📌 Cambios no commitados. Revisión manual pendiente."
fi
```

> 💡 **No olvides hacerlo ejecutable:**

```bash
chmod +x scripts/sync-old-repo.sh
```

---

## 🗂️ `scripts/README.md`

````md
# 🧰 Scripts de Utilidad del Proyecto

Este directorio contiene scripts auxiliares para facilitar tareas comunes de desarrollo.

---

## 📦 `sync-old-repo.sh`

### 🧠 Propósito

Sincroniza el contenido del entorno `Give-OLD/` al entorno actual del repositorio, excluyendo la carpeta `.git`, con el fin de recuperar archivos importantes sin alterar el historial de versiones.

### 🛠 Uso

```bash
./scripts/sync-old-repo.sh
````

El script:

1. Usa `rsync` para copiar los archivos.
2. Verifica el estado del repositorio con `git status`.
3. Pregunta si querés agregar y commitear los cambios automáticamente.

### 🔐 Seguridad

La carpeta `.git` del entorno viejo no se copia, evitando conflictos de historial o referencias cruzadas.

---

````

---

## 👤 Desarrollador principal

**Jesús Abregú**  
*Full Stack Developer | DevOps*  
💬 Apasionado por el código limpio, el impacto social y la automatización con propósito.

> 🧠 **Idea original:** Miguel Agui  
> 🛠️ **Líder de proyecto y mantenimiento actual:** Jesús Abregú

---

## 📬 Contacto

¿Tenés ideas, sugerencias o simplemente querés charlar?

- 📧 **Email:** abjes785@gmail.com  
- 🌐 (https://www.linkedin.com/in/abjes)*  
- 🐙 (https://github.com/JesusAbregu/test-angular-ssr)

---

## 📄 `abjes.md` – Presentación personal

```md
# abjes.md - Presentación de Jesús Abregú

**Nombre:** Jesús Abregú  
**Rol:** Full Stack Developer | DevOps  
**Experiencia:** +10 años desarrollando soluciones escalables y automatización de infraestructura.

Estoy muy entusiasmado de sumarme al equipo de **Give-What-You-No-Longer-Use**. Mi foco estará en:

- Integración continua (CI)
- Configuración de entornos de desarrollo
- Escalabilidad y seguridad del sistema

Estoy disponible para coordinar tareas técnicas, contribuir a la planificación y acompañar las siguientes etapas del proyecto.

Gracias por la bienvenida 🙌. Estoy comprometido a aportar lo mejor de mi experiencia y seguir construyendo en equipo.

---

### 🔁 Sincronización entre entornos

📅 El **5 de julio**, se realizó una **migración manual** desde el entorno `Give-OLD/` al entorno activo `Give-What-You-No-Longer-Use/`, conservando archivos relevantes que no habían sido versionados originalmente debido a:

- Errores de permisos
- Exclusiones en `.gitignore`
- Omisión de `git add`

📂 Archivos importantes recuperados:
- `abjes.md` (con timestamp anterior)
- `docker-compose.yml`
- Archivos PHP (no versionados previamente)

🛠️ Se utilizó `rsync --exclude='.git'` para evitar conflictos de historial, preservando únicamente los archivos de trabajo y manteniendo intacta la carpeta `.git` del nuevo entorno.


Estoy muy entusiasmado de sumarme al equipo de **Give-What-You-No-Longer-Use**. Mi foco estará en:

- Integración continua (CI)
- Configuración de entornos de desarrollo
- Escalabilidad y seguridad del sistema

Estoy disponible para coordinar tareas técnicas, contribuir a la planificación y acompañar las siguientes etapas del proyecto.

Gracias por la bienvenida 🙌. Estoy comprometido a aportar lo mejor de mi experiencia y seguir construyendo en equipo.

---

### 🔁 Sincronización entre entornos

📅 El **5 de julio**, se realizó una **migración manual** desde el entorno `Give-OLD/` al entorno activo `Give-What-You-No-Longer-Use/`, conservando archivos relevantes que no habían sido versionados originalmente debido a:

- Errores de permisos
- Exclusiones en `.gitignore`
- Omisión de `git add`

📂 Archivos importantes recuperados:
- `abjes.md` (con timestamp anterior)
- `docker-compose.yml`
- Archivos PHP (no versionados previamente)

🛠️ Se utilizó `rsync --exclude='.git'` para evitar conflictos de historial, preservando únicamente los archivos de trabajo y manteniendo intacta la carpeta `.git` del nuevo entorno.
````

---

