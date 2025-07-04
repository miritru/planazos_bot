from datetime import datetime
from telegram.ext import ConversationHandler, MessageHandler, CommandHandler, filters
from storage import cargar_planes, guardar_planes
from utils import usuario_permitido
from config import BORRAR_ELEGIR, USUARIOS_PERMITIDOS

async def anadir(update, context):
    if not usuario_permitido(update):
        await update.message.reply_text("🚫 Lo siento, no tienes permiso para usar este bot.")
        return

    try:
        texto = ' '.join(context.args)
        print("Texto recibido:", texto)  # debug
        if not texto:
            raise ValueError("No hay texto después del comando")
        fecha_str, *descripcion = texto.split(' ', 1)
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        descripcion = descripcion[0] if descripcion else 'Sin descripción'

        nuevo_plan = {
            'fecha': fecha.strftime("%Y-%m-%d"),
            'descripcion': descripcion,
            'usuario': update.effective_user.username or "anónimo"
        }

        planes = cargar_planes()
        planes.append(nuevo_plan)
        guardar_planes(planes)

        await update.message.reply_text(f"✅ Plan añadido para el {fecha_str}: {descripcion}")
    except Exception as e:
        print("Error en anadir:", e)
        await update.message.reply_text("❌ Formato incorrecto. Usa: /anadir 15/07/2025 Cena con amigos")

async def delete_start(update, context):
    if not usuario_permitido(update):
        await update.message.reply_text("🚫 Lo siento, no tienes permiso para usar este bot.")
        return ConversationHandler.END

    if not context.args:
        await update.message.reply_text("❌ Debes poner la fecha del plan a borrar. Ej: /delete 15/07/2025")
        return ConversationHandler.END

    fecha_str = context.args[0]
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        await update.message.reply_text("❌ Fecha inválida. Usa formato DD/MM/YYYY.")
        return ConversationHandler.END

    planes = cargar_planes()
    planes_en_fecha = [p for p in planes if p['fecha'] == fecha]

    if not planes_en_fecha:
        await update.message.reply_text(f"📭 No hay planes para la fecha {fecha_str}.")
        return ConversationHandler.END

    # Guardamos la lista en context para usar después
    context.user_data['planes_a_borrar'] = planes_en_fecha

    mensaje = f"Planes en {fecha_str}:\n"
    for i, plan in enumerate(planes_en_fecha, 1):
        usuario = plan.get('usuario', 'desconocido')
        mensaje += f"{i}. {plan['descripcion']} (añadido por @{usuario})\n"
    mensaje += "\nResponde con el número del plan que quieres borrar."

    await update.message.reply_text(mensaje)
    return BORRAR_ELEGIR

async def delete_elegir(update, context):
    seleccion = update.message.text.strip()

    if not seleccion.isdigit():
        await update.message.reply_text("❌ Por favor, responde con un número válido.")
        return BORRAR_ELEGIR

    indice = int(seleccion) - 1
    planes = context.user_data.get('planes_a_borrar')

    if indice < 0 or indice >= len(planes):
        await update.message.reply_text("❌ Número fuera de rango. Intenta otra vez.")
        return BORRAR_ELEGIR

    plan_a_borrar = planes[indice]

    # Cargar todos los planes y eliminar el elegido
    todos_planes = cargar_planes()
    todos_planes = [p for p in todos_planes if p != plan_a_borrar]
    guardar_planes(todos_planes)

    await update.message.reply_text(f"✅ Plan '{plan_a_borrar['descripcion']}' del {plan_a_borrar['fecha']} borrado.")

    # Limpiar user_data
    context.user_data.pop('planes_a_borrar', None)

    return ConversationHandler.END

async def delete_cancel(update, context):
    await update.message.reply_text("❌ Operación cancelada.")
    return ConversationHandler.END

async def proximos(update, context):
    if not usuario_permitido(update):
        await update.message.reply_text("🚫 Lo siento, no tienes permiso para usar este bot.")
        return

    hoy = datetime.now()
    planes = cargar_planes()
    planes_futuros = [p for p in planes if datetime.strptime(p['fecha'], "%Y-%m-%d") >= hoy]

    if not planes_futuros:
        await update.message.reply_text("📭 No hay planes futuros.")
        return

    planes_futuros.sort(key=lambda x: x['fecha'])
    mensaje = "📅 Próximos planes:\n"
    for p in planes_futuros:
        fecha = datetime.strptime(p['fecha'], "%Y-%m-%d").strftime("%d/%m/%Y")
        usuario = p.get('usuario', 'desconocido')
        mensaje += f"• {fecha}: {p['descripcion']} (añadido por @{usuario})\n"
    await update.message.reply_text(mensaje)

async def pasados(update, context):
    if not usuario_permitido(update):
        await update.message.reply_text("🚫 Lo siento, no tienes permiso para usar este bot.")
        return

    try:
        hoy = datetime.now()
        años = int(context.args[0]) if context.args else 1
        limite = hoy.replace(year=hoy.year - años)

        planes = cargar_planes()
        planes_pasados = [
            p for p in planes
            if limite <= datetime.strptime(p['fecha'], "%Y-%m-%d") < hoy
        ]

        if not planes_pasados:
            await update.message.reply_text(f"📭 No hay planes pasados en los últimos {años} año(s).")
            return

        planes_pasados.sort(key=lambda x: x['fecha'], reverse=True)
        mensaje = f"📜 Planes pasados (últimos {años} año(s)):\n"
        for p in planes_pasados:
            fecha = datetime.strptime(p['fecha'], "%Y-%m-%d").strftime("%d/%m/%Y")
            usuario = p.get('usuario', 'desconocido')
            mensaje += f"• {fecha}: {p['descripcion']} (añadido por @{usuario})\n"
        await update.message.reply_text(mensaje)

    except Exception:
        await update.message.reply_text("❌ Usa: /pasados [número de años]. Ej: /pasados 2")

async def help_command(update, context):
    mensaje = (
        "🤖 *Comandos disponibles:*\n\n"
        "/anadir DD/MM/YYYY descripción - Añade un plan nuevo.\n"
        "/proximos - Muestra los planes futuros.\n"
        "/pasados [años] - Muestra los planes pasados (por defecto 1 año).\n"
        "/delete DD/MM/YYYY - Borrar un plan en la fecha indicada.\n"
        "/help - Muestra este mensaje de ayuda."
    )
    await update.message.reply_text(mensaje, parse_mode='Markdown')

async def start(update, context):
    username = update.effective_user.username
    if username not in USUARIOS_PERMITIDOS:
        await update.message.reply_text("🚫 Lo siento, no tienes permiso para usar este bot.")
        return

    mensaje = (
        f"¡Hola, @{username}! 👋\n\n"
        "Este es tu bot de planes. Aquí puedes:\n"
        "/anadir DD/MM/YYYY descripción - Añadir un plan.\n"
        "/proximos - Ver próximos planes.\n"
        "/pasados [años] - Ver planes pasados (por defecto 1 año).\n"
        "/delete DD/MM/YYYY - Borrar un plan en la fecha indicada.\n"
        "/help - Mostrar ayuda para uso de comandos.\n\n"
        "¡Disfruta! 🎉"
    )
    await update.message.reply_text(mensaje)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('delete', delete_start)],
    states={
        BORRAR_ELEGIR: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_elegir)],
    },
    fallbacks=[CommandHandler('cancel', delete_cancel)],
)
