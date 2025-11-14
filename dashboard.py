import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import os

# ==================== CARGAR DATOS ====================
print("="*60)
print("📊 CARGANDO DATOS PARA EL DASHBOARD")
print("="*60)

if not os.path.exists('quotes_data.pkl'):
    print("\n❌ ERROR: No se encontró el archivo 'quotes_data.pkl'")
    print("👉 Por favor, ejecuta primero 'scraping.py' para obtener los datos.")
    print("="*60)
    exit()

try:
    df = pd.read_pickle('quotes_data.pkl')
    print(f"✓ Cargadas {len(df)} citas correctamente")
except Exception as e:
    print(f"\n❌ Error al cargar los datos: {e}")
    exit()

# ==================== PREPARAR DATOS ====================
# Explotar tags para análisis
df_tags = df.explode('tags')

# Extraer año de nacimiento y convertir a siglo romano
df['anio_nacimiento'] = df['author_birthdate'].dt.year

def anio_a_siglo_romano(anio):
    """Convierte un año a su siglo en números romanos según la RAE"""
    numero_siglo = (anio - 1) // 100 + 1
    # Conversión a números romanos
    mapa_romano = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X',
        40: 'XL', 50: 'L', 90: 'XC', 100: 'C'
    }
    resultado = ''
    for valor in sorted(mapa_romano.keys(), reverse=True):
        while numero_siglo >= valor:
            resultado += mapa_romano[valor]
            numero_siglo -= valor
    return f'siglo {resultado}'

df['siglo_nacimiento'] = df['anio_nacimiento'].apply(anio_a_siglo_romano)

print(f"✓ Datos procesados correctamente")
print("="*60 + "\n")

# ==================== CREAR DASHBOARD ====================
app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.DARKLY, dbc.icons.FONT_AWESOME], 
           suppress_callback_exceptions=True, title="Citas famosas")

# Variable para almacenar el tema actual
tema_actual = 'light'

# Estilos personalizados
ESTILO_TARJETA = {
    'box-shadow': '0 4px 6px rgba(0,0,0,0.1)',
    'border-radius': '10px',
    'padding': '20px',
    'margin-bottom': '20px'
}

app.layout = dbc.Container([
    # Store para el tema
    dcc.Store(id='almacen-tema', data='light'),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("📚 Dashboard de citas de personajes famosos", 
                       className="text-center mb-2",
                       style={'color': '#2c3e50', 'font-weight': 'bold'},
                       id='titulo-principal'),
                html.P(f"Análisis de {len(df)} citas de {df['author'].nunique()} autores",
                      className="text-center mb-4",
                      id='subtitulo')
            ])
        ], width=10),
        dbc.Col([
            dbc.Button(
                html.I(className="fas fa-moon"),
                id="boton-tema",
                color="secondary",
                className="mt-3",
                n_clicks=0,
                title="Cambiar tema"
            )
        ], width=2, className="text-end")
    ]),
    
    # Filtros
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🔍 Filtros", className="mb-3"),
                    
                    html.Label("Buscar en citas:", className="fw-bold"),
                    dcc.Input(
                        id='entrada-busqueda',
                        type='text',
                        placeholder='Escribe para buscar...',
                        className='form-control mb-3',
                        debounce=True
                    ),
                    
                    html.Label("Autor:", className="fw-bold"),
                    dcc.Dropdown(
                        id='desplegable-autor',
                        options=[{'label': 'Todos', 'value': 'all'}] + 
                                [{'label': autor, 'value': autor} for autor in sorted(df['author'].unique())],
                        value='all',
                        placeholder='Selecciona un autor',
                        clearable=False,
                        className='mb-3'
                    ),
                    
                    html.Label("Etiqueta:", className="fw-bold"),
                    dcc.Dropdown(
                        id='desplegable-etiqueta',
                        options=[{'label': 'Todas', 'value': 'all'}] + 
                                [{'label': etiqueta, 'value': etiqueta} for etiqueta in sorted(df_tags['tags'].unique()) if etiqueta.strip()],
                        value='all',
                        placeholder='Selecciona una etiqueta',
                        clearable=False,
                        className='mb-3'
                    ),
                ])
            ], style=ESTILO_TARJETA)
        ], width=12)
    ]),
    
    # Métricas principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='total-citas', className="text-center text-primary"),
                    html.P("Citas encontradas", className="text-center text-muted")
                ])
            ], style=ESTILO_TARJETA)
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='total-autores', className="text-center text-success"),
                    html.P("Autores únicos", className="text-center text-muted")
                ])
            ], style=ESTILO_TARJETA)
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3(id='total-etiquetas', className="text-center text-warning"),
                    html.P("Etiquetas únicas", className="text-center text-muted")
                ])
            ], style=ESTILO_TARJETA)
        ], width=4),
    ], className="mb-4"),
    
    # Gráficos
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 Top 10 autores más citados", className="mb-3"),
                    dcc.Graph(id='grafico-autores')
                ])
            ], style=ESTILO_TARJETA)
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🏷️ Etiquetas más populares", className="mb-3"),
                    dcc.Graph(id='grafico-etiquetas')
                ])
            ], style=ESTILO_TARJETA)
        ], width=6),
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📅 Distribución por siglo de nacimiento", className="mb-3"),
                    dcc.Graph(id='grafico-siglos')
                ])
            ], style=ESTILO_TARJETA)
        ], width=12),
    ]),
    
    # Lista de citas
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("💬 Citas filtradas (mostrando hasta 20)", className="mb-3"),
                    html.Div(id='lista-citas')
                ])
            ], style=ESTILO_TARJETA)
        ], width=12)
    ]),
    
], fluid=True, style={'padding': '20px', 'background-color': '#f8f9fa'}, id='contenedor-principal')

# ==================== CALLBACK PARA TEMA ====================
@app.callback(
    [Output('almacen-tema', 'data'),
     Output('contenedor-principal', 'style'),
     Output('titulo-principal', 'style'),
     Output('subtitulo', 'style'),
     Output('boton-tema', 'children')],
    [Input('boton-tema', 'n_clicks')],
    [Input('almacen-tema', 'data')]
)
def alternar_tema(n_clicks, tema_actual):
    # Determinar el tema actual
    if n_clicks % 2 == 0:
        # Tema claro
        estilo_contenedor = {'padding': '20px', 'background-color': '#f8f9fa'}
        estilo_titulo = {'color': '#2c3e50', 'font-weight': 'bold'}
        estilo_subtitulo = {'color': '#6c757d'}
        icono = html.I(className="fas fa-moon")
        tema = 'light'
    else:
        # Tema oscuro
        estilo_contenedor = {'padding': '20px', 'background-color': '#1a1a1a', 'color': '#e0e0e0'}
        estilo_titulo = {'color': '#e0e0e0', 'font-weight': 'bold'}
        estilo_subtitulo = {'color': '#b0b0b0'}
        icono = html.I(className="fas fa-sun")
        tema = 'dark'
    
    return tema, estilo_contenedor, estilo_titulo, estilo_subtitulo, icono

# ==================== CALLBACKS ====================
@app.callback(
    [Output('total-citas', 'children'),
     Output('total-autores', 'children'),
     Output('total-etiquetas', 'children'),
     Output('grafico-autores', 'figure'),
     Output('grafico-etiquetas', 'figure'),
     Output('grafico-siglos', 'figure'),
     Output('lista-citas', 'children')],
    [Input('entrada-busqueda', 'value'),
     Input('desplegable-autor', 'value'),
     Input('desplegable-etiqueta', 'value')]
)
def actualizar_dashboard(texto_busqueda, autor_seleccionado, etiqueta_seleccionada):
    # Filtrar datos
    df_filtrado = df.copy()
    
    # Manejar valores None o vacíos de los dropdowns
    if autor_seleccionado is None or autor_seleccionado == '':
        autor_seleccionado = 'all'
    if etiqueta_seleccionada is None or etiqueta_seleccionada == '':
        etiqueta_seleccionada = 'all'
    
    if texto_busqueda:
        df_filtrado = df_filtrado[
            df_filtrado['quote'].str.contains(texto_busqueda, case=False, na=False) |
            df_filtrado['author'].str.contains(texto_busqueda, case=False, na=False)
        ]
    
    if autor_seleccionado != 'all':
        df_filtrado = df_filtrado[df_filtrado['author'] == autor_seleccionado]
    
    if etiqueta_seleccionada != 'all':
        df_filtrado = df_filtrado[df_filtrado['tags'].apply(lambda x: etiqueta_seleccionada in x)]
    
    # Métricas
    total_citas = len(df_filtrado)
    total_autores = df_filtrado['author'].nunique()
    df_etiquetas_filtrado = df_filtrado.explode('tags')
    total_etiquetas = df_etiquetas_filtrado['tags'].nunique()
    
    # Gráfico de autores - Verificar que hay datos
    if total_citas > 0:
        conteo_autores = df_filtrado['author'].value_counts().head(10)
        fig_autores = px.bar(
            x=conteo_autores.values,
            y=conteo_autores.index,
            orientation='h',
            labels={'x': 'Número de citas', 'y': 'Autor'},
            color=conteo_autores.values,
            color_continuous_scale='Blues'
        )
        fig_autores.update_layout(
            showlegend=False,
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis={'categoryorder': 'total ascending'}
        )
    else:
        fig_autores = go.Figure()
        fig_autores.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig_autores.update_layout(height=400)
    
    # Gráfico de tags - Verificar que hay datos y filtrar vacíos
    if total_citas > 0 and len(df_etiquetas_filtrado) > 0:
        # Filtrar tags vacíos antes de contar
        conteo_etiquetas = df_etiquetas_filtrado[df_etiquetas_filtrado['tags'].str.strip() != '']['tags'].value_counts().head(15)
        if len(conteo_etiquetas) > 0:
            fig_etiquetas = px.bar(
                x=conteo_etiquetas.index,
                y=conteo_etiquetas.values,
                labels={'x': 'Etiqueta', 'y': 'Frecuencia'},
                color=conteo_etiquetas.values,
                color_continuous_scale='Viridis'
            )
            fig_etiquetas.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis={'tickangle': -45}
            )
        else:
            fig_etiquetas = go.Figure()
            fig_etiquetas.add_annotation(
                text="No hay datos para mostrar",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            fig_etiquetas.update_layout(height=400)
    else:
        fig_etiquetas = go.Figure()
        fig_etiquetas.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig_etiquetas.update_layout(height=400)
    
    # Gráfico de siglos - Verificar que hay datos
    if total_citas > 0:
        conteo_siglos = df_filtrado['siglo_nacimiento'].value_counts().sort_index()
        fig_siglos = px.pie(
            values=conteo_siglos.values,
            names=conteo_siglos.index,
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_siglos.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0)
        )
    else:
        fig_siglos = go.Figure()
        fig_siglos.add_annotation(
            text="No hay datos para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        fig_siglos.update_layout(height=400)
    
    # Lista de citas
    componentes_citas = []
    for idx, fila in df_filtrado.head(20).iterrows():
        tarjeta_cita = dbc.Card([
            dbc.CardBody([
                html.P(fila["quote"], 
                      className="fst-italic mb-2",
                      style={'font-size': '1.1em'}),
                html.Hr(),
                html.Div([
                    html.Strong(fila['author']),
                    html.Span(f" • {fila['author_birthdate'].strftime('%d/%m/%Y')}", 
                             className="text-muted ms-2"),
                    html.Span(f" • {fila['author_birthplace']}", 
                             className="text-muted ms-2"),
                ]),
                html.Div([
                    dbc.Badge(etiqueta, color="primary", className="me-1") 
                    for etiqueta in fila['tags']
                ], className="mt-2"),
                html.Details([
                    html.Summary("Ver biografía", 
                                style={'cursor': 'pointer', 'color': '#007bff', 
                                      'font-size': '0.9em', 'margin-top': '10px'}),
                    html.Hr(),
                    html.P(fila['author_about'], className="small text-muted mb-0")
                ])
            ])
        ], className="mb-3", style={'border-left': '4px solid #007bff'})
        
        componentes_citas.append(tarjeta_cita)
    
    if not componentes_citas:
        componentes_citas = [html.P("No se encontraron citas con los filtros seleccionados.", 
                                   className="text-center text-muted")]
    
    return (
        str(total_citas),
        str(total_autores),
        str(total_etiquetas),
        fig_autores,
        fig_etiquetas,
        fig_siglos,
        componentes_citas
    )

# ==================== EJECUTAR ====================
if __name__ == '__main__':
    print("="*60)
    print("🚀 INICIANDO DASHBOARD")
    print("="*60)
    print("📍 Abre tu navegador en: http://127.0.0.1:8050")
    print("🔄 Para detener el servidor: Ctrl+C")
    print("="*60 + "\n")
    
    app.run(debug=False, port=8050)