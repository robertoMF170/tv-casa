# TV Casa — lista de canais

Lista de canais oficiais gratuitos (PT) usada pela app **TV Casa**.
A app vai buscar `canais.json` aqui ao arrancar; se falhar, usa a cópia embutida na APK.

- **Validação**: o GitHub Actions testa os streams todos os dias às 06:30 (Lisboa) e guarda o resultado em `estado.json` — sem PC, sem VPS.
- **Mudar canais**: editar `canais.json` e fazer push; a app atualiza-se sozinha na próxima abertura.

Canais oficiais gratuitos: RTP 1/2/3/Memória/Açores/Madeira, SIC, SIC Notícias, TVI, CNN Portugal.
