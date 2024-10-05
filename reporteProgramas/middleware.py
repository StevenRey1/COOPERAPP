from django.shortcuts import redirect
from .models import Reporte

class ProgresoReporteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la ruta solicitada
        path = request.path

        # Verificar si la ruta solicitada es parte del proceso de creación del reporte
        if ('crear-datos-quien-reporta' in path or 'crear-datos-cooperante' in path or 'crear-logros-avances' in path or 
            'crear-apoyo-eventos' in path or 'crear-apoyo-viajes' in path or 'crear-apoyo-territorios' in path or
            'crear-apoyo-contratacion' in path or 'crear-apoyo-material' in path or 'crear-apoyo-herramientas' in path or
            'crear-apoyo-litigio' in path or 'crear-apoyo-seguridad-alimentaria' in path or 'crear-apoyo-ordenes-judiciales' in path or
            'crear-apoyo-archivo-historico' in path or 'crear-otros-apoyos' in path or 'crear-estimacion-economica' in path):
            # Obtener el reporte_id desde la URL
            reporte_id = None
            try:
                reporte_id = int(path.split('/')[-2])
            except (ValueError, IndexError):
                pass

            if reporte_id:
                try:
                    # Obtener el reporte desde la base de datos
                    reporte = Reporte.objects.get(id=reporte_id)

                    # Verificar en qué paso del proceso está el reporte
                    if reporte.avance == 0 and 'crear-datos-quien-reporta' not in path:
                        # Si no ha completado los datos de quien reporta, redirigir a esa vista
                        return redirect('reporteProgramas:crear_datos_quien_reporta', reporte_id=reporte.id)
                    
                    elif reporte.avance == 1 and 'crear-acercamiento' not in path and reporte.tipo==1:
                        return redirect('reporteAcercamientos:crear_acercamiento', reporte_id=reporte.id)
                        
                    elif reporte.avance == 1 and 'crear-datos-cooperante' not in path and reporte.tipo==2:
                        # Si no ha completado el acercamiento, redirigir a la vista de crear acercamiento
                        return redirect('reporteProgramas:crear_datos_cooperante', reporte_id=reporte.id)
                    
                    elif reporte.avance == 2 and 'crear-necesidades' not in path and reporte.tipo==1:
                        return redirect('reporteAcercamientos:crear_necesidades', reporte_id=reporte.id)

                    elif reporte.avance == 2 and 'crear-logros-avances' not in path and reporte.tipo==2:

                        linea_accion = reporte.datoscooperante.linea_accion.id

                        # Si no ha completado las necesidades, redirigir a la vista de crear necesidades
                        return redirect('reporteProgramas:crear_logros_avances', reporte_id=reporte.id, linea_accion_id=linea_accion)
                    elif reporte.avance == 3 and 'crear-apoyo-eventos' not in path:
                        # Si no ha completado los apoyos de eventos, redirigir a la vista de crear apoyos de eventos
                        return redirect('reporteAportes:crear_apoyo_eventos', reporte_id=reporte.id)
                    elif reporte.avance == 4 and 'crear-apoyo-viajes' not in path:

                        return redirect('reporteAportes:crear_apoyo_viajes', reporte_id=reporte.id)
                    elif reporte.avance == 5 and 'crear-apoyo-territorios' not in path:
                            
                        return redirect('reporteAportes:crear_apoyo_territorios', reporte_id=reporte.id)
                    elif reporte.avance == 6 and 'crear-apoyo-contratacion' not in path:
                                
                        return redirect('reporteAportes:crear_apoyo_contratacion', reporte_id=reporte.id)
                    elif reporte.avance == 7 and 'crear-apoyo-material' not in path:
                                    
                        return redirect('reporteAportes:crear_apoyo_material', reporte_id=reporte.id)
                    
                    elif reporte.avance == 8 and 'crear-apoyo-herramientas' not in path:
                                            
                        return redirect('reporteAportes:crear_apoyo_herramientas', reporte_id=reporte.id)
                    elif reporte.avance ==  9 and 'crear-apoyo-litigio' not in path:

                        return redirect('reporteAportes:crear_apoyo_litigio', reporte_id=reporte.id)
                    elif reporte.avance == 10 and 'crear-apoyo-seguridad-alimentaria' not in path:
                            
                        return redirect('reporteAportes:crear_apoyo_seguridad_alimentaria', reporte_id=reporte.id)
                    elif reporte.avance == 11 and 'crear-apoyo-ordenes-judiciales' not in path:

                        return redirect('reporteAportes:crear_apoyo_ordenes_judiciales', reporte_id=reporte.id)
                    elif reporte.avance == 12 and 'crear-apoyo-archivo-historico' not in path:
                            
                        return redirect('reporteAportes:crear_apoyo_archivo_historico', reporte_id=reporte.id)
                    elif reporte.avance == 13 and 'crear-otros-apoyos' not in path:
                                
                        return redirect('reporteAportes:crear_otros_apoyos', reporte_id=reporte.id)
                    elif reporte.avance == 14 and 'crear-estimacion-economica' not in path:
                        return redirect('reporteAportes:crear_estimacion_economica', reporte_id=reporte.id)


                except Reporte.DoesNotExist:
                    # Si el reporte no existe, puedes redirigir a una página de error o manejar la excepción
                    return redirect('error_404')  # Redirigir a una vista de error 404 si no se encuentra el reporte

        # Continuar con la solicitud normal si no es parte del proceso
        response = self.get_response(request)
        return response