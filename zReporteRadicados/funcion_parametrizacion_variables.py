
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
            ,radicados.usuario_radico
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
                ,t1.usuario_radico
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
    select distinct consulta_1.radicado 
            ,consulta_1.usuario_responsable_actividad_anterior
            ,consulta_1.actividad_actual_tramite
            ,consulta_1.usuario_actual_responsable_tramite
            ,consulta_1.con_plano_cartografico
            ,consulta_1.usuario_inserta_plano
            ,consulta_1.npn
            ,consulta_1.municipio
            ,consulta_1.ficha
            ,consulta_1.pversion
            ,consulta_1.componente_responsable
            ,consulta_1.fase_actividad
            ,(case when consulta_1.npn = consulta_2.numero_predial_formal then 'Formal'
                when consulta_1.npn = consulta_2.numero_predial_informal then 'Informal'
                when consulta_1.npn <> consulta_2.numero_predial_informal and substring(consulta_1.npn from 22 for 1) = '2' then 'Posible Informalidad'
                when consulta_1.npn <> consulta_2.numero_predial_informal and substring(consulta_1.npn from 30 for 1) <> '0' then 'Posible Informalidad'
                else 'Posible Formal o Predio Nuevo'	 	       
            end) tipo_terreno
    from 
    (
    --
        select distinct t2.radicado 
            ,t2.usuario_responsable_actividad_anterior
            ,t2.actividad_actual_tramite
            ,t2.usuario_actual_responsable_tramite
            ,t2.con_plano_cartografico
            ,t2.usuario_inserta_plano
            ,t2.npn
            ,t2.municipio
            ,t2.ficha
            ,t2.pversion
            ,(case when t2.actividad_actual_tramite in ('Consolidando información'
                                                        ,'Incorporando predios a la versión'
                                                        ,'Realizando visita de campo'
                                                        ,'Revisando Información Reconocimiento  Inicial'
                                                        ,'Revisando Información'
                                                        ,'Realizando Transacción Catastral'
                                                        ,'Revisando Información'
                                                        ,'Revisando Información Final Reconocimiento') then 'Reconocimiento'
                when t2.actividad_actual_tramite in ('Realizando Análisis Catastro Registro') then 'Jurídica'
                when t2.actividad_actual_tramite in ('Preparando Edición Geográfica'
                                                    ,'Realizando Edición Geográfica'
                                                    ,'Revisando Información Geográfica') then 'SIG'
                when t2.actividad_actual_tramite in ('Revisando Información Calidad'
                                                    ,'Revisando Información Terreno'
                                                    ,'Realizando Revisión Informe de Aseguramiento'
                                                    ,'Aprobando y consolidacion XTF'                                                    
                                                    ,'Realizando Entrega de Productos Finales') then 'Calidad'
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
                    when actividad_actual_tramite in ('Realizando Transacción Catastral'
                                                    ,'Revisando Información'
                                                    ,'Revisando Información Calidad'
                                                    ,'Revisando Información Terreno'
                                                    ,'Revisando Información Final Reconocimiento'
                                                    ,'Realizando Revisión Informe de Aseguramiento'
                                                    ,'Aprobando y consolidacion XTF'                                                    
                                                    ,'Realizando Entrega de Productos Finales') then 'En Transacción Catastral o Posterior'
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
            ,t1.ficha
            ,t1.pversion 
            from bpmcat.vw_trmactivos_rad_npn_plano t1 
            where nom_tramite = 'Formación y Actualización'
        ) t2
    ) consulta_1
    left join 
    (
        -- Total de Informalidades por Predio Formal
        select numero_predial_formal
            ,numero_predial_informal
            ,nro_radicado
            ,nro_version
            ,nro_ficha_prd_informal
        from version.vw_bcgs_prd_informales
    ) consulta_2
    on concat(consulta_1.npn, consulta_1.radicado) = concat(consulta_2.numero_predial_formal, cast(consulta_2.nro_radicado AS text))
        or concat(consulta_1.npn, consulta_1.radicado) = concat(consulta_2.numero_predial_informal, cast(consulta_2.nro_radicado AS text));
    """
    
    consulta_fechas = """ 
        select distinct t1.radicado
            ,cast(t1.fecha_radicado as date) fecha_radicado
            ,cast(t2.dt_adt_fchupd as date) fecha_actualizacion_tramite
        from bpmcat.vw_rpt_tramites_en_proceso t1 
        left join bpmcat.tb_bpm_egn_proegn t2 on t1.radicado = t2.vr_proegn_rad;
        """
    
    renombrar_actividades = {'Incorporando predios a la versión':'1.Incorporando predios a la versión'
        ,'Realizando Análisis Catastro Registro':'2.Realizando Análisis Catastro Registro'
        ,'Realizando visita de campo':'3.Realizando visita de campo'
        ,'Consolidando información':'4.Consolidando información'        
        ,'Revisando Información Reconocimiento  Inicial':'5.Revisando Información Reconocimiento Inicial'        
        ,'Preparando Edición Geográfica':'6.Preparando Edición Geográfica'
        ,'Realizando Edición Geográfica':'7.Realizando Edición Geográfica'
        ,'Revisando Información Geográfica':'8.Revisando Información Geográfica'
        ,'Realizando Transacción Catastral':'9.Realizando Transacción Catastral'
        ,'Revisando Información':'10.Revisando Información'
        ,'Revisando Información Final Reconocimiento':'11.Revisando Información Final Reconocimiento'
        ,'Revisando Información Calidad':'12.Revisando Información Calidad'
        ,'Revisando Información Terreno':'13.Revisando Información Terreno'
        ,'Realizando Revisión Informe de Aseguramiento':'14.Realizando Revisión Informe de Aseguramiento'
        ,'Aprobando y consolidacion XTF':'15.Aprobando y consolidacion XTF'
        ,'Realizando Entrega de Productos Finales':'16.Realizando Entrega de Productos Finales'
        }
    
    dict_coordinador_reconocedor = {'abel.maldonado':'Reconocedor'
        ,'adner.capella':'Reconocedor'
        ,'abel.maldonado':'Reconocedor'
        ,'aida.belalcazar':'SIG'
        ,'albeiro.marulanda':'Reconocedor'
        ,'alvaro.donado':'Reconocedor'
        ,'amed.blandon':'SIG'
        ,'andres.ramos':'SIG'
        ,'andres.salgado':'Jurídico'
        ,'angel.banquez':'Reconocedor'
        ,'angelica.ponce':'SIG'
        ,'camilo.moreno':'SIG'
        ,'celci.quintana':'Reconocedor'
        ,'denilson.correa':'Reconocedor'
        ,'diana.pineda':'SIG'
        ,'edinson.vergara':'Reconocedor'
        ,'eduard.gomez':'Calidad'
        ,'emilio.castillo':'Reconocedor'
        ,'erich.sarabia':'Calidad'
        ,'euclides.polo':'Reconocedor'
        ,'fabian.arango':'Reconocedor'
        ,'fabio.barragan':'Reconocedor'
        ,'felipe.rodriguez':'Reconocedor'
        ,'francisco.galarcio':'Reconocedor'
        ,'fredy.solorzano':'Reconocedor'
        ,'gabriel.bustamante':'Líder Calidad'
        ,'german.panizza':'Reconocedor'
        ,'gustavo.maldonado':'Reconocedor'
        ,'harlingto.padilla':'Reconocedor'
        ,'hernando.sarmiento':'Reconocedor'
        ,'jacqueline.jimenez':'Coordinador'
        ,'jair.benedetty':'Coordinador'
        ,'jarod.macareno':'Reconocedor'
        ,'javier.romero':'Reconocedor'
        ,'jerry.bedoya':'Reconocedor'
        ,'jorge.avendano':'Calidad'
        ,'jorge.hernandez':'Reconocedor'
        ,'jorge.menco': 'Líder Reconocimiento'
        ,'juan.herreraa':'SIG'
        ,'juan.otero':'SIG'
        ,'julie.castano':'Líder Jurídico'
        ,'julio.buendia':'SIG'
        ,'karen.escobar':'Reconocedor'
        ,'kevin.castro':'Coordinador'
        ,'liney.arroyo':'Coordinador'
        ,'luis.jimenez':'Reconocedor'
        ,'maria.hernandez':'Reconocedor'
        ,'maria.montaña':'Calidad'
        ,'maria.vasquez':'Calidad'
        ,'marlon.martinez':'SIG'
        ,'mary.conquett':'Reconocedor'
        ,'melany.delahoz':'Jurídico'
        ,'monica.penuela':'Reconocedor'
        ,'nadith.miranda':'Reconocedor'
        ,'nilsen.arteta':'Reconocedor'
        ,'pedro.garcia':'Reconocedor'
        ,'rafael.molina':'Reconocedor'
        ,'ricardo.guerrero':'Reconocedor'
        ,'ricardo.pacheco':'SIG'
        ,'samith.saenz':'Reconocedor'
        ,'sandra.acosta':'Reconocedor'
        ,'soporte4':'Reconocedor'
        ,'soporte5':'Reconocedor'
        ,'stefany.dominguez':'Reconocedor'
        ,'william.perez':'Reconocedor'
        ,'wilmar.ruiza':'Reconocedor'
        ,'yeinez.cortes':'Reconocedor'
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
    
    consulta_interesado_sexo = """
        select t1.codigo_dane
        ,t1.numero_predial
        ,t1.sexo
        from 
        (
        select distinct substring(numero_predial,1,5) codigo_dane
        ,numero_predial
        ,tipo_documento
        ,sexo
        from bpmcat.vw_bcgs_interesados
        where tipo_documento <> 'NIT'
        ) t1;
    """

    consulta_sexo_npn = """select distinct substring(numero_predial,1,5) codigo_dane
        ,numero_predial
        ,tipo_documento
        ,sexo
        ,grupo_etnico
        from bpmcat.vw_bcgs_interesados
        where tipo_documento <> 'NIT';
    """

    consulta_tRendimientosDevueltosActualizacion = """
        select distinct t2.radicado 
            ,t2.usuario_responsable_actividad_anterior
            ,t2.actividad_actual_tramite
            ,t2.usuario_actual_responsable_tramite
            ,t2.con_plano_cartografico
            ,t2.usuario_inserta_plano
            ,t2.npn
            ,t2.municipio
            ,t2.ficha
            ,t2.pversion
            ,(case when t2.actividad_actual_tramite in ('Consolidando información'
                                                        ,'Incorporando predios a la versión'
                                                        ,'Realizando visita de campo'
                                                        ,'Revisando Información Reconocimiento  Inicial'
                                                        ,'Revisando Información'
                                                        ,'Realizando Transacción Catastral'
                                                        ,'Revisando Información'
                                                        ,'Revisando Información Final Reconocimiento') then 'Reconocimiento'
                when t2.actividad_actual_tramite in ('Realizando Análisis Catastro Registro') then 'Jurídica'
                when t2.actividad_actual_tramite in ('Preparando Edición Geográfica'
                                                    ,'Realizando Edición Geográfica'
                                                    ,'Revisando Información Geográfica') then 'SIG'
                when t2.actividad_actual_tramite in ('Revisando Información Calidad'
                                                    ,'Revisando Información Terreno'
                                                    ,'Realizando Revisión Informe de Aseguramiento'
                                                    ,'Aprobando y consolidacion XTF'                                                    
                                                    ,'Realizando Entrega de Productos Finales') then 'Calidad'
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
                    when actividad_actual_tramite in ('Realizando Transacción Catastral'
                                                    ,'Revisando Información'
                                                    ,'Revisando Información Calidad'
                                                    ,'Revisando Información Terreno'
                                                    ,'Revisando Información Final Reconocimiento'
                                                    ,'Realizando Revisión Informe de Aseguramiento'
                                                    ,'Aprobando y consolidacion XTF'                                                    
                                                    ,'Realizando Entrega de Productos Finales') then 'En Transacción Catastral o Posterior'
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
        ,t1.ficha
        ,t1.pversion 
        from bpmcat.vw_trmdevuelto_rad_npn_plano t1
        where nom_tramite = 'Formación y Actualización'
        ) t2;
        """
    
    consulta_informalidades = """
        select distinct t1.numero_predial_formal
            ,t1.numero_predial_informal
            ,t2.total_informalidades
        from version.vw_bcgs_prd_informales t1
        inner join 
        (
            -- Total de Informalidades por Predio Formal
            select distinct numero_predial_formal
                ,count(*) total_informalidades
            from version.vw_bcgs_prd_informales
            group by 1
        ) t2
        on t2.numero_predial_formal = t1.numero_predial_formal;
        """
    
    dict_area_municipio = {'MariaLaBaja':56102.4,
        'Repelon':35834.4,
        'Baranoa':12124.4,
        'Sabanagrande':4306.6}
    
    consulta_interesados = """
    select t1.numero_predial_nacional
    ,t1.tipo_predio
    ,t1.orip
    ,t1.matrl matricula_inmobiliaria
    ,t1.destino_economico
    ,t2.tipo_derecho
    ,t2.derecho fraccion_derecho
    ,t2.fecha_tenencia
    ,t2.tipo_documento
    ,t2.documento numero_documento
    ,t2.nombre_interesado
    ,t1.fecha_visita
    from (
        select numero_predial_nacional
        ,tipo_predio
        ,orip
        ,matrl
        ,destino_economico
        ,cast(fecha_visita as date) fecha_visita
        from "version".vw_predios_levantamiento
    ) t1
    left join 
    (
    select distinct nro_radicado
        ,tipo_derecho
        ,derecho
        ,cast(fecha_tenencia as date) fecha_tenencia
        ,nro_ficha 
        ,numero_predial
        ,tipo_documento	
        ,documento
        ,nombre_interesado
    from bpmcat.vw_bcgs_interesados
    ) t2
    on t1.numero_predial_nacional = t2.numero_predial;
    """

    dict_capa_version = {'m442.210':['m442','bcgs_geo.m442.r_lc_terreno'], # ? Maria La Baja [Rural]
        'm442.215':['m442','bcgs_geo.m442.u_lc_terreno'], # ? Maria La Baja [Urbano]
        'm606.410':['m606','bcgs_geo.m606.r_lc_terreno'], # ? Repelón [Rural]
        'm606.634':['m606','bcgs_geo.m606.u_lc_terreno'] # ? Repelón [Urbano]
    }

    consulta_creadorRadicado = """
        select distinct radicado
        ,usuario_radico
        from bpmcat.vw_rpt_tramites_en_proceso
        where vr_nombre_proceso = 'Formación y Actualización';
    """

    consulta_predio_interesado_derecho = """
        select pred.numero_predial_nacional
            ,(case when pred.vr_npn_mncpio = '442' then 'MariaLaBaja'
            when pred.vr_npn_mncpio = '606' then 'Repelon'
            when pred.vr_npn_mncpio = '634' then 'Sabanagrande'
            when pred.vr_npn_mncpio = '078' then 'Baranoa'
            else pred.vr_npn_mncpio
            end) nombre_municipio
            ,pred.tipo_predio
            ,pred.nb_predio_direcc direccion_predio
            ,pred.orip
            ,pred.matrl folio_matricula
            ,pred.novedad_npn
            ,pred.novedad_folio_matricula	
            ,pred.area_catastral_terreno
            ,pred.area_registral	
            ,cast(pred.fecha_visita as date) fecha_visita
            ,pred.beneficio_comun_indigenas
            ,t1.tipo_documento
            ,t1.numero_documento
            ,t1.nombre_interesado
            ,t1.sexo
            ,t1.grupo_etnico
            ,t1.rnc_campesino
            ,t1.tipo_derecho
            ,t1.porcentaje_derecho
            ,t1.fecha_inicio_tenencia
            ,t1.tipo_fuente
            ,t1.fuente
        from "version".vw_predios_levantamiento pred left join
            (
            
                    select inter.numero_predial
                    ,inter.tipo_documento
                    ,inter.documento numero_documento
                    ,inter.nombre_interesado
                    ,inter.sexo
                    ,inter.grupo_etnico
                    ,inter.rnc_campesino
                    ,inter.tipo_derecho
                    ,inter.derecho porcentaje_derecho
                    ,cast(inter.fecha_tenencia as date) fecha_inicio_tenencia
                    ,inter.tipo_fuente
                    ,inter.fuente
                    from bpmcat.vw_bcgs_interesados inter
            ) t1 on
        pred.numero_predial_nacional = t1.numero_predial;
    """

    return consulta_tRadicados, consuta_tFinalizados, consulta_tRendimientosActualizacion, consulta_fechas, renombrar_actividades, dict_coordinador_reconocedor, consulta_radicado_hijo, consulta_nro_ficha, nombre_procesos, consulta_interesado_sexo, consulta_sexo_npn, consulta_tRendimientosDevueltosActualizacion, consulta_informalidades, dict_area_municipio, consulta_interesados, dict_capa_version, consulta_creadorRadicado, consulta_predio_interesado_derecho #[17]