## Script de Inclusão de Tags IMDb

Este script, desenvolvido por mim, permite buscar automaticamente filmes no IMDb (Internet Movie Database) com base em arquivos ".mkv" e incluir tags relevantes. O script utiliza a API do OMDB para obter dados de filmes do IMDb e realiza as operações necessárias de tagging.

### Recursos
- Busca filmes no IMDb com base no nome do arquivo e ano de lançamento.
- Recupera dados de filmes usando a API do OMDB.
- Inclui tags do IMDb no formato XML.
- Adiciona tags globais nos arquivos ".mkv" utilizando o `mkvpropedit`.
- Remove datas de codificação dos arquivos ".mkv".

### Pré-requisitos
Antes de executar o script, certifique-se de ter o seguinte:
- Uma chave de API do OMDB, que deve ser definida como valor da variável `OMDB_API_KEY` no script.
- A ferramenta `mkvpropedit`, que deve estar instalada e acessível no PATH do sistema.

### Utilização
1. Digite a localização da pasta contendo os arquivos ".mkv" quando solicitado.
2. O script irá procurar por cada arquivo ".mkv" na pasta especificada, recuperar informações do filme no IMDb e incluir as tags correspondentes.
3. As tags do IMDb serão salvas em um arquivo XML chamado "imdb_info.xml" no diretório de saída.
4. O script irá adicionar as tags globais em cada arquivo ".mkv" utilizando o `mkvpropedit`.
5. As datas de codificação serão removidas dos arquivos ".mkv" modificados.

Observação: Certifique-se de atualizar a variável `OMDB_API_KEY` e o campo "Encoder" antes de executar o script.

**Importante:** Verifique se você possui uma conexão de internet estável e se a chave da API do OMDB é válida para recuperar dados de filmes do IMDb.

Versão: 0.09 (Whatever Will Be, Will Be)

Para obter mais detalhes e atualizações, consulte o script neste repositório.
