# Segurança

## Credenciais

Nunca registre tokens do SonarQube, GitHub, Atlas ou outros serviços. Manifests podem referenciar `${VARIAVEL}`, mas o valor deve vir do ambiente do desenvolvedor ou de um secret manager.

## Supply chain

- Fixe dependências APM por tag literal ou SHA completo.
- Consumidores corporativos devem preferir SHA completo e manter o comentário/metadata da versão humana.
- Fixe imagens de container por versão aprovada; para maior garantia, a plataforma pode substituir a tag por digest.
- A versão do APM usada no CI fica fixa em `atlas.yml` e deve ser atualizada por PR revisada.
- Workflows e actions de terceiros exigem revisão da plataforma; em produção, fixe actions por SHA.

## Reporte

Use o canal privado de segurança da organização. Não abra issue pública contendo vulnerabilidade, token, URL interna ou dados de cliente.

