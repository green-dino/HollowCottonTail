# playbook/utils.py
import os 
import json
from django.conf import settings
import graphviz as gv
from pyvis.network import Network


class PlaybookUtils:
    @staticmethod
    def validate_input(play_name, roles, blocks, tasks):
        """
        Validate playbook input data.

        Args:
            play_name (str): Name of the play.
            roles (list): List of roles.
            blocks (list): List of blocks.
            tasks (list): List of tasks.

        Returns:
            errors (list): List of validation errors.
        """
        errors = []
        if not play_name:
            errors.append("Play name is required.")
        if not roles:
            errors.append("At least one role is required.")
        if not blocks:
            errors.append("At least one block is required.")
        if not tasks:
            errors.append("At least one task is required.")
        if any(not item for item in roles + blocks + tasks):
            errors.append("All entries must contain at least one item.")
        return errors

    @staticmethod
    def save_playbook_to_file(playbook_data, version, author, filename="playbook.json"):
        """
        Save playbook data to a JSON file.

        Args:
            playbook_data (dict): Playbook data to save.
            version (str): Version of the playbook.
            author (str): Author of the playbook.
            filename (str): Name of the file to save the playbook in.
        """
        playbook_data.update({"version": version, "author": author})
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        try:
            with open(filepath, "w") as file:
                json.dump(playbook_data, file)
            return True, "Playbook saved successfully."
        except TypeError as e:
            return False, f"Error saving playbook: {e}"

    @staticmethod
    def load_playbook_from_file(filename="playbook.json"):
        """
        Load playbook data from a JSON file.

        Args:
            filename (str): Name of the file to load the playbook from.

        Returns:
            tuple: (status, playbook_data or error_message)
        """
        filepath = settings.MEDIA_ROOT / filename
        try:
            with open(filepath, "r") as file:
                playbook_data = json.load(file)
                return True, playbook_data
        except FileNotFoundError:
            return False, "Playbook file not found."
        except json.JSONDecodeError as e:
            return False, f"Error loading playbook: {e}"

class PlaybookGraphCreator:
    """
    Class to create a playbook graph using Graphviz.
    """
    def __init__(self, play_name, roles, blocks, tasks):
        self.dot = gv.Digraph()
        with self.dot.subgraph(name='cluster_playbook') as playbook:
            playbook.attr(label='Playbook')
            playbook.node('Play', play_name)
            self._add_nodes(playbook, roles, 'Role')
            self._add_nodes(playbook, blocks, 'Block')
            self._add_nodes(playbook, tasks, 'Task')

    def _add_nodes(self, playbook, items, prefix):
        for item in items:
            node_id = f'{prefix}_{item}'
            playbook.node(node_id, item)
            playbook.edge('Play', node_id)

    def get_dot(self):
        """
        Get the Graphviz dot representation of the playbook graph.

        Returns:
            dot (graphviz.Digraph): Graphviz dot object.
        """
        return self.dot

class InteractiveGraphCreator:
    @staticmethod
    def create_interactive_graph(play_name, roles, blocks, tasks):
        """
        Create an interactive graph using Pyvis.

        Args:
            play_name (str): Name of the play.
            roles (list): List of roles.
            blocks (list): List of blocks.
            tasks (list): List of tasks.

        Returns:
            net (pyvis.network.Network): Pyvis network object.
        """
        net = Network(directed=True)
        net.add_node(play_name, label=play_name, color='red', size=25)
        InteractiveGraphCreator._add_nodes(net, roles, play_name, 'blue')
        InteractiveGraphCreator._add_nodes(net, blocks, play_name, 'green')
        InteractiveGraphCreator._add_nodes(net, tasks, play_name, 'orange')
        return net

    @staticmethod
    def _add_nodes(net, items, parent, color):
        for item in items:
            net.add_node(item, label=item, color=color)
            net.add_edge(parent, item)