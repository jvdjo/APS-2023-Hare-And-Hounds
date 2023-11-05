import sys
from tkinter import Tk, Menu

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy


class Menubar(Menu):
    _tk: Tk
    _server_proxy: PyNetgamesServerProxy
    _connect_dropdown: Menu
    _match_dropdown: Menu

    def __init__(self, server_proxy: PyNetgamesServerProxy, tk: Tk, **kwargs) -> None:
        super().__init__(tk, **kwargs)
        self._tk = tk
        self._server_proxy = server_proxy
        self._connect_dropdown = self._build_connect_dropdown()
        self._match_dropdown = self._build_match_dropdown()

    def connection_confirmed(self):
        self._connect_dropdown.entryconfig("Disconnect", state="normal")
        self._connect_dropdown.entryconfig("Connect", state="disabled")
        self._match_dropdown.entryconfig("Request Match", state="normal")

    def connection_error(self, error: Exception):
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="normal")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def disconnect(self):
        self._server_proxy.send_disconnect()
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="normal")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def _build_connect_dropdown(self):
        connect = Menu(self, tearoff=0)
        connect.add_command(label="Connect", command=self._connect)
        connect.add_command(label="Disconnect", command=self.disconnect, state='disabled')
        connect.add_separator()
        connect.add_command(label="Exit", command=sys.exit)
        self.add_cascade(label="Connection", menu=connect)
        return connect

    def _connect(self):
        self._server_proxy.send_connect(address="wss://py-netgames-server.fly.dev")
        self._connect_dropdown.entryconfig("Disconnect", state="disabled")
        self._connect_dropdown.entryconfig("Connect", state="disabled")
        self._match_dropdown.entryconfig("Request Match", state="disabled")

    def _build_match_dropdown(self):
        match = Menu(self, tearoff=0)
        match.add_command(label="Request Match", command=self._request_match, state='disabled')
        self.add_cascade(label="Match", menu=match)
        return match

    def _request_match(self):
        self._server_proxy.send_match(amount_of_players=2)