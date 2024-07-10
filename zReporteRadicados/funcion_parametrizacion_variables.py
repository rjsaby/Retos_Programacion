
# ? PARAMETRIZACIÓN DE VARIABLES

def parametrizacion_variables():

    # TODO: Consulta sobre -vw_trmactivos_rad_npn- y -vw_rpt_tramites_en_proceso-
    consulta_tRadicados = """ 
        select distinct t0.*
            ,radicados."Proceso"
            ,radicados.vr_nombre_proceso
            ,radicados.estado_tramite
            ,radicados.actividad
            ,radicados.vr_estado_paso
            ,radicados.proceso_estado
            ,radicados.fecha_radicado
            ,radicados.usuario
            ,radicados.vr_proces_des
            ,radicados.vr_consec_nom
            ,radicados.vr_consec_des
            ,radicados.vr_consec_tip
            ,radicados.vr_step_est
            ,radicados.vr_task_nom
            ,radicados.vr_task_tip
            ,radicados.vr_task_con
            ,radicados.vr_task_est
        from bpmcat.vw_trmactivos_rad_npn t0
        inner join (
            select distinct t1.municipio
                ,t1.npn
                ,t1.nro_ficha
                ,t1.radicado
                ,(case when t1.vr_nombre_proceso like 'Comple%%' then 'Conservación'
                    when t1.vr_nombre_proceso like 'Forma%%' then 'Actualización'
                    when t1.vr_nombre_proceso like 'Muta%%' then 'Conservación'				
                    when t1.vr_nombre_proceso like 'Recti%%' then 'Conservación'
                    else t1.vr_nombre_proceso
                    end) "Proceso"
                ,t1.vr_nombre_proceso	
                ,t1.estado_tramite
                ,t1.actividad
                ,t1.vr_estado_paso
                ,t2.vr_proegn_est proceso_estado
                ,t2.nb_step_idn
                ,cast(t2.dt_adt_fchupd as date) dt_adt_fchupd
                ,t2.vr_proegn_ori
                ,cast(t1.fecha_radicado as date) fecha_radicado
                ,t1.usuario
                ,cast(t2.dt_adt_fchupd as date) fecha_actualizacion_tramite
                ,t3.vr_proces_des
                ,t6.vr_consec_nom
                ,t6.vr_consec_des
                ,t6.vr_consec_tip
                ,t4.vr_step_est
                --,t4.nb_task_idn
                ,t5.vr_task_nom 
                ,t5.vr_task_tip
                ,t5.vr_task_con
                ,t5.vr_task_est 
                ,t7.vr_functy_des
            from bpmcat.vw_rpt_tramites_en_proceso t1
            left join bpmcat.tb_bpm_egn_proegn t2 on t1.radicado = t2.vr_proegn_rad
            left join bpmcat.tb_bpm_mdl_proces t3 on t2.nb_proces_idn = t3.nb_proces_idn 
            left join bpmcat.tb_fw_sec_consec t6 on t3.nb_consec_idn = t6.nb_consec_idn 
            left join bpmcat.tb_bpm_egn_step t4 on t2.nb_step_idn = t4.nb_step_idn
            left join bpmcat.tb_bpm_mdl_task t5 on t4.nb_task_idn = t5.nb_task_idn
            left join bpmcat.tb_fw_gui_functy t7 on t5.nb_functy_idn = t7.nb_functy_idn
            ) radicados 
        on radicados.radicado = t0.radicado;
        """
    
    consuta_tFinalizados = """
        select distinct t1.municipio
            ,t1.npn
            ,t1.nro_ficha
            ,t1.radicado
            ,(case when t1.vr_nombre_proceso like 'Comple%%' then 'Conservación'
                when t1.vr_nombre_proceso like 'Forma%%' then 'Actualización'
                when t1.vr_nombre_proceso like 'Muta%%' then 'Conservación'				
                when t1.vr_nombre_proceso like 'Recti%%' then 'Conservación'
                else t1.vr_nombre_proceso
                end) "Proceso"
            ,t1.vr_nombre_proceso
            ,cast(t1.fecha_radicado as date) fecha_radicado
            ,cast(t1.fecha_finalizacion as date) fecha_finalizacion
            ,t1.resolucion
            ,t1.fecha_resolucion
            --,t1.nb_proegn_idn
            ,t2.vr_proegn_est proceso_estado
            --,t2.nb_step_idn
            --,cast(t2.dt_adt_fchupd as date) dt_adt_fchupd
            ,t2.vr_proegn_ori
            --,t2.nb_proces_idn
            --,t3.vr_proces_nom 
            ,t3.vr_proces_des
            ,t6.vr_consec_nom
            ,t6.vr_consec_des
            ,t6.vr_consec_tip
            ,t4.vr_step_est
            --,t4.nb_task_idn
            ,t5.vr_task_nom 
            ,t5.vr_task_tip
            ,t5.vr_task_con
            ,t5.vr_task_est 
            ,t7.vr_functy_des	
        from bpmcat.vw_rpt_tramites_finalizados t1
        left join tb_bpm_egn_proegn t2 on t1.nb_proegn_idn = t2.nb_proegn_idn
        left join tb_bpm_mdl_proces t3 on t2.nb_proces_idn = t3.nb_proces_idn 
        left join tb_fw_sec_consec t6 on t3.nb_consec_idn = t6.nb_consec_idn 
        left join tb_bpm_egn_step t4 on t2.nb_step_idn = t4.nb_step_idn
        left join tb_bpm_mdl_task t5 on t4.nb_task_idn = t5.nb_task_idn
        left join tb_fw_gui_functy t7 on t5.nb_functy_idn = t7.nb_functy_idn;
        """
    
    consulta_tRendimientosActualizacion = """
        select distinct t2.radicado 
            ,t2.usuario_responsable_actividad_anterior
            ,t2.actividad_actual_tramite
            ,t2.usuario_actual_responsable_tramite
            ,t2.con_plano_cartografico
            ,t2.usuario_inserta_plano
            ,t2.npn
            ,t2.municipio
            ,(case when t2.actividad_actual_tramite in ('Consolidando información'
                                                        ,'Incorporando predios a la versión'
                                                        ,'Realizando visita de campo'
                                                        ,'Revisando Información Reconocimiento  Inicial'
                                                        ,'Revisando Información'
                                                        ,'Realizando Transacción Catastral') then 'Reconocimiento'
                when t2.actividad_actual_tramite in ('Realizando Análisis Catastro Registro') then 'Jurídica'
                when t2.actividad_actual_tramite in ('Preparando Edición Geográfica'
                                                    ,'Realizando Edición Geográfica'
                                                    ,'Revisando Información Geográfica') then 'SIG'
                else 'Sin parametrización'
                end) componente_responsable
            ,(case when actividad_actual_tramite in ('Consolidando información'
                                                    ,'Incorporando predios a la versión'
                                                    ,'Realizando visita de campo'
                                                    ,'Revisando Información Reconocimiento  Inicial'
                                                    ,'Realizando Análisis Catastro Registro'
                                                    ,'Preparando Edición Geográfica'
                                                    ,'Realizando Edición Geográfica'
                                                    ,'Revisando Información Geográfica') then 'Fase Previa a la Transacción Catastral'
                    when actividad_actual_tramite in ('Realizando Transacción Catastral',
                                                    'Revisando Información') then 'En Transacción Catastral o Posterior'
                else 'Sin parametrización'
                end) fase_actividad
                
        from
        (
        select distinct t1.radicado
        ,t1.user_fn_activiad_ant usuario_responsable_actividad_anterior
        ,t1.actividad actividad_actual_tramite
        ,t1.user_actividad_act usuario_actual_responsable_tramite
        ,t1.plano_cartografico con_plano_cartografico
        ,t1.user_inserta_plano usuario_inserta_plano
        ,t1.npn 
        ,t1.municipio 
        from bpmcat.vw_trmactivos_rad_npn_plano t1
        where nom_tramite = 'Formación y Actualización'
        ) t2;
        """
    
    consulta_fechas = """ 
        select distinct t1.radicado
            ,cast(t1.fecha_radicado as date) fecha_radicado
            ,cast(t2.dt_adt_fchupd as date) fecha_actualizacion_tramite
        from bpmcat.vw_rpt_tramites_en_proceso t1 
        left join bpmcat.tb_bpm_egn_proegn t2 on t1.radicado = t2.vr_proegn_rad;
        """
    
    renombrar_actividades = {'Consolidando información':'4.Consolidando información'
                        ,'Incorporando predios a la versión':'1.Incorporando predios a la versión'
                        ,'Realizando visita de campo':'3.Realizando visita de campo'
                        ,'Revisando Información Reconocimiento  Inicial':'5.Revisando Información Reconocimiento Inicial'
                        ,'Realizando Análisis Catastro Registro':'2.Realizando Análisis Catastro Registro'
                        ,'Preparando Edición Geográfica':'6.Preparando Edición Geográfica'
                        ,'Realizando Edición Geográfica':'7.Realizando Edición Geográfica'
                        ,'Revisando Información Geográfica':'8.Revisando Información Geográfica'
                        ,'Realizando Transacción Catastral':'9.Realizando Transacción Catastral'
                        ,'Revisando Información Calidad':'10.Revisando Información Calidad'
                        }
    
    dict_coordinador_reconocedor = {
        'abel.maldonado':'Reconocedor'
        ,'aida.belalcazar':'SIG'
        ,'albeiro.marulanda':'Reconocedor'
        ,'alvaro.donado':'Reconocedor'
        ,'amed.blandon':'SIG'
        ,'andres.ramos':'SIG'
        ,'angel.banquez':'Reconocedor'
        ,'camilo.moreno':'SIG'
        ,'celci.quintana':'Reconocedor'
        ,'diana.pineda':'SIG'
        ,'emilio.castillo':'Reconocedor'
        ,'euclides.polo':'Reconocedor'
        ,'fabian.arango':'Reconocedor'
        ,'fabio.barragan':'Reconocedor'
        ,'francisco.galarcio':'Reconocedor'
        ,'german.panizza':'Reconocedor'
        ,'harlingto.padilla':'Reconocedor'
        ,'hernando.sarmiento':'Reconocedor'
        ,'jacqueline.jimenez':'Coordinador'
        ,'jair.benedetty':'Coordinador'
        ,'jarod.macareno':'Reconocedor'
        ,'jorge.avendano':'Calidad'
        ,'jorge.hernandez':'Reconocedor'
        ,'juan.herreraa':'SIG'
        ,'juan.otero':'SIG'
        ,'julie.castano':'Jurídico'
        ,'karen.escobar':'Reconocedor'
        ,'kevin.castro':'Coordinador'
        ,'liney.arroyo':'Coordinador'
        ,'luis.jimenez':'Reconocedor'
        ,'maria.hernandez':'Reconocedor'
        ,'maria.montaña':'Calidad'
        ,'mary.conquett':'Reconocedor'
        ,'melany.delahoz':'Jurídico'
        ,'monica.penuela':'Reconocedor'
        ,'nadith.miranda':'Reconocedor'
        ,'pedro.garcia':'Reconocedor'
        ,'rafael.molina':'Reconocedor'
        ,'ricardo.guerrero':'Reconocedor'
        ,'samith.saenz':'Reconocedor'
        ,'soporte4':'Reconocedor'
        ,'stefany.dominguez':'Reconocedor'
        ,'william.perez':'Reconocedor'
        ,'yesmy.batista':'Reconocedor'
        }
    
    consulta_radicado_hijo = """
        select distinct radicado_padre
            ,radicado
        from bpmcat.v_rdcd_pdr_hijo_actualizacion
    """

    consulta_nro_ficha = """
        select distinct radicado
	        ,nro_ficha 
        from bpmcat.vw_rpt_tramites_en_proceso;
    """
    
    nombre_procesos = ['Complementación - Nomenclatura, Matrícula y Propietario',
        'Mutaciones de Primera Clase',
        'Mutaciones de Segunda Clase',
        'Mutaciones de Tercera Clase',
        'Mutaciones de Cuarta Clase',
        'Mutaciones de Quinta Clase',        
        'Rectificación de Cabida y Linderos 1101']

    return consulta_tRadicados, consuta_tFinalizados, consulta_tRendimientosActualizacion, consulta_fechas, renombrar_actividades, dict_coordinador_reconocedor, consulta_radicado_hijo, consulta_nro_ficha, nombre_procesos