# playbook/views.py
from django.shortcuts import render
from .forms import PlaybookForm
from .utils import PlaybookUtils, PlaybookGraphCreator, InteractiveGraphCreator

def playbook_view(request):
    if request.method == 'POST':
        form = PlaybookForm(request.POST)
        if form.is_valid():
            play_name = form.cleaned_data['play_name']
            roles = form.cleaned_data['roles'].split(',')
            blocks = form.cleaned_data['blocks'].split(',')
            tasks = form.cleaned_data['tasks'].split(',')
            version = form.cleaned_data['version']
            author = form.cleaned_data['author']

            # Validate and save playbook
            errors = PlaybookUtils.validate_input(play_name, roles, blocks, tasks)
            if errors:
                return render(request, 'playbook/playbook_form.html', {'form': form, 'errors': errors})

            # Create and display the graph
            playbook_data = {
                "play_name": play_name,
                "roles": roles,
                "blocks": blocks,
                "tasks": tasks
            }
            PlaybookUtils.save_playbook_to_file(playbook_data, version, author)

            graph_creator = PlaybookGraphCreator(play_name, roles, blocks, tasks)
            interactive_graph = InteractiveGraphCreator.create_interactive_graph(play_name, roles, blocks, tasks)
            interactive_graph.write_html('static/playbook_graph.html')

            return render(request, 'playbook/playbook_result.html', {
                'playbook_data': playbook_data,
                'graph_dot': graph_creator.get_dot(),
                'interactive_graph_url': '/static/playbook_graph.html'
            })

    else:
        form = PlaybookForm()

    return render(request, 'playbook/playbook_form.html', {'form': form})
