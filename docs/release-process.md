# Processo de release

## Pull request

`validate.yml` calcula os pacotes afetados. Uma mudança em `tools/`, policy, configuração ou workflows revalida todos os pacotes.

As quatro classes de verificação são:

1. **Estrutura:** manifests, nomes, frontmatter, owners e arquivos referenciados.
2. **Release:** incremento de versão, changelog e tag ainda não publicada.
3. **Segurança:** segredos, Unicode oculto, executáveis, dependências, MCPs e permissões.
4. **Funcionamento:** auditoria APM e instalação real em projeto Kiro temporário, verificando os arquivos gerados.

Testes comportamentais ficam em `tests/cases.yml`. Eles descrevem entradas e resultados observáveis; não devem testar apenas palavras ou cabeçalhos do `SKILL.md`.

## Merge na main

`release.yml` usa o SHA exato do evento. Ele identifica manifests cuja tag de versão ainda não existe, revalida e publica primeiro skills e depois kits.

Idempotência:

- tag ausente: cria tag anotada e GitHub Release;
- tag no mesmo SHA: não move a tag e completa apenas artefatos ausentes;
- tag em outro SHA: falha e exige investigação.

O workflow cria tag, release e metadata no mesmo encadeamento. Não depende de um segundo workflow disparado pelo push da tag.

## Sincronização do kit

Depois de uma release individual, `sync-kit.yml` executa `tools/sync_kit.py` e abre uma PR:

- adiciona todas as skills oficiais presentes na `main`;
- atualiza as refs para as tags individuais;
- incrementa minor se o conjunto mudou;
- incrementa patch se apenas versões internas mudaram;
- atualiza changelog;
- deixa o CI instalar o kit inteiro e detectar conflitos.

Essa PR pode receber automerge somente se a organização decidir que a classe de mudança é elegível e os checks/revisões obrigatórios forem preservados.

## Rollback

Nunca mova a tag defeituosa. Publique uma nova versão corrigida ou abra PRs nos consumidores voltando para o SHA anterior do kit. O Atlas usa o registro de adoção para localizar projetos afetados.
