import tkinter as tk
from tkinter import ttk

class Node:
    def __init__(self, name):
        self.name = name
        self.routing_table = {name: 0}  # Costo a sé stesso è 0
        self.next_hop = {name: None}  # Next hop a sé stesso è None
        self.neighbors = {}

    def add_neighbor(self, neighbor, cost):
        """Aggiungi un nodo vicino alla lista dei vicini con il relativo costo."""
        self.neighbors[neighbor.name] = (neighbor, cost)  # Memorizza il nodo vicino e il costo
        self.routing_table[neighbor.name] = cost  # Aggiungi il costo per il vicino
        self.next_hop[neighbor.name] = neighbor.name  # Il next hop inizialmente è il vicino stesso

    def receive_routing_info(self, neighbor_name, neighbor_table):
        """
        Riceve le informazioni di routing da un vicino e aggiorna la propria tabella
        se necessario, restituendo True se la tabella è stata aggiornata.
        """
        updated = False
        for dest, cost_to_dest in neighbor_table.items():
            # Calcola il nuovo costo passando attraverso il vicino
            new_cost = self.neighbors[neighbor_name][1] + cost_to_dest
            if dest not in self.routing_table or self.routing_table[dest] > new_cost:
                self.routing_table[dest] = new_cost
                self.next_hop[dest] = neighbor_name  # Aggiorna il next hop
                updated = True
        return updated  # Ritorna True se la tabella è stata aggiornata

    def send_routing_info(self):
        """Restituisce il nome del nodo e la sua tabella di routing."""
        return self.name, self.routing_table

class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_name):
        """Aggiungi un nodo alla rete se non esiste già."""
        if node_name not in self.nodes:
            self.nodes[node_name] = Node(node_name)
        else:
            print(f"Attenzione: Nodo {node_name} esiste già!")

    def add_link(self, node1_name, node2_name, cost):
        """Aggiungi un collegamento tra due nodi con il relativo costo."""
        if node1_name not in self.nodes or node2_name not in self.nodes:
            print(f"Errore: Uno o entrambi i nodi {node1_name}, {node2_name} non esistono.")
            return
        node1, node2 = self.nodes[node1_name], self.nodes[node2_name]
        node1.add_neighbor(node2, cost)
        node2.add_neighbor(node1, cost)

    def update_routing_tables(self):
        """
        Aggiorna le tabelle di routing per tutti i nodi finché non ci sono più cambiamenti.
        Ottimizzazione: esce quando nessuna tabella è cambiata.
        """
        updates = True
        while updates:
            updates = False
            for node in self.nodes.values():
                # Propagazione delle tabelle dai vicini
                for neighbor in node.neighbors.values():
                    neighbor_name, neighbor_table = neighbor[0].send_routing_info()
                    if node.receive_routing_info(neighbor_name, neighbor_table):
                        updates = True

    def get_routing_tables(self):
        """Restituisce le tabelle di routing per tutti i nodi."""
        routing_tables = {}
        for node in self.nodes.values():
            routing_tables[node.name] = {
                "destination": {dest: cost for dest, cost in node.routing_table.items()},
                "next_hop": {dest: node.next_hop[dest] for dest in node.routing_table}
            }
        return routing_tables

    def print_routing_tables(self):
        """Stampa le tabelle di routing finali per ogni nodo."""
        for node in self.nodes.values():
            print(f"TABELLA DI ROUTING DEL NODO {node.name}:")
            print(f"{'DESTINAZIONE':<15}{'COSTO':<10}{'Next Hop'}")  # Header
            for dest in sorted(node.routing_table):
                cost = node.routing_table[dest]
                next_hop = node.next_hop[dest]
                print(f"{dest:<15}{cost:<10}{next_hop}")  # Formattazione tabellare
            print()

    def show_routing_tables_gui(self):
        """Mostra una GUI con le tabelle di routing."""
        root = tk.Tk()
        root.title("Tabelle di Routing")

        # Crea un notebook per i tab
        notebook = ttk.Notebook(root)

        # Ordina i nomi dei nodi in ordine alfabetico
        for node_name, table in sorted(self.get_routing_tables().items()):
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=f"Nodo {node_name}")

            tree = ttk.Treeview(frame, columns=("Destinazione", "Costo", "Next Hop"), show="headings")
            tree.heading("Destinazione", text="Destinazione")
            tree.heading("Costo", text="Costo")
            tree.heading("Next Hop", text="Next Hop")

            # Ordina le destinazioni in ordine alfabetico
            for dest, cost in sorted(table["destination"].items()):
                next_hop = table["next_hop"][dest]
                tree.insert("", "end", values=(dest, cost, next_hop))

            tree.pack(expand=True, fill="both")

        notebook.pack(expand=True, fill="both")
        root.mainloop()

# Creazione della rete
network = Network()

# Aggiunta dei nodi
for node_name in ["A", "B", "C", "D"]:
    network.add_node(node_name)

# Definizione dei collegamenti (link) con relativi costi
network.add_link("A", "B", 2)
network.add_link("A", "C", 3)
network.add_link("B", "C", 1)
network.add_link("B", "D", 6)
network.add_link("C", "D", 5)

# Aggiornamento delle tabelle di routing
network.update_routing_tables()

# Stampa finale delle tabelle di routing
network.print_routing_tables()

# Mostra la GUI
network.show_routing_tables_gui()
