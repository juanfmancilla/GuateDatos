from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from .forms import CommentForm
import plotly.express as px
import pandas as pd
import datetime

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'


def create_interactive_graph(post, figures_to_show):
    plot_div = None
    if post.slug == 'ejemplo':
        # Leer los archivos de datos
        gdp = pd.read_csv("./static/world_bank.csv", skiprows=4)
        temps = pd.read_csv("./static/temperaturas_1991_2016_GTM.csv")

        # Preparacion de datos
        gdp.rename(columns={'Country Name': 'Pais',
                            'Country Code': 'codPais',
                            'Indicator Name': 'Indicador',
                            'Indicator Code': 'codIndicador'},
                   inplace=True)

        # Poner en formato "Tidy"
        gdp = pd.melt(gdp, id_vars=['Pais', 'codPais', 'Indicador', 'codIndicador'], var_name='Año')
        gdp.rename(columns={'value': 'GDP'}, inplace=True)

        # Poner la fecha en el formato DateTime
        temps.Mes = temps.Mes.str.strip()  # Los meses tienen espacios en blanco, quitarselos
        temps.Mes = temps.Mes.apply(lambda x: datetime.datetime.strptime(x, "%b").month)  # Convertir mes a num
        temps["Fecha"] = pd.to_datetime(dict(year=temps.Anio, month=temps.Mes, day=28))

        # desplegar graficas

        temp_graph = px.line(temps, x="Fecha", y="Temp(Celsius)",
                             title="Temperaturas mensuales promedio",
                             height=400,
                             )
        temp_graph.update_xaxes(rangeslider_visible=True)

        box_graph = px.box(data_frame=temps
                           , x="Mes"
                           , y="Temp(Celsius)"
                           , notched=True
                           , title="Distribución de temperaturas por mes"
                           , template='presentation'
                           )
        plot_div = temp_graph.to_html() + "\n" + box_graph.to_html()
    return plot_div


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    figures_to_show = request.POST.getlist('tag')
    plot_div = create_interactive_graph(post, figures_to_show)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'plot_div': plot_div})

