# Controle de release

Última atualização: 2026-09-24 (America/Sao_Paulo).

## Estado atual

- Branch de produção: `main`.
- Commit integrado: `67eaf36fe96bd21cc8432955e170db7841541be2`.
- Pull request: [#1](https://github.com/williamwinwill/atlas-nuclea-ia/pull/1), aprovado pelo solicitante e integrado.
- Validação pós-merge: [GitHub Actions 36081002119](https://github.com/williamwinwill/atlas-nuclea-ia/actions/runs/36081002119), concluída com sucesso.
- Publicação: [GitHub Actions 36081002143](https://github.com/williamwinwill/atlas-nuclea-ia/actions/runs/36081002143), concluída com sucesso.
- Sincronização do kit: [GitHub Actions 36081098918](https://github.com/williamwinwill/atlas-nuclea-ia/actions/runs/36081098918), concluída sem alteração pendente.
- Deploy de aplicação: não se aplica; este repositório distribui pacotes por tags imutáveis e GitHub Releases.

## Pacotes publicados

| Pacote | Versão | Tag | GitHub Release |
|---|---:|---|---|
| `pipeline-review` | 1.1.0 | `pipeline-review--v1.1.0` | publicada |
| `sonar-fix` | 1.1.0 | `sonar-fix--v1.1.0` | publicada |
| `terraform-review` | 1.1.0 | `terraform-review--v1.1.0` | publicada |
| `atlas-all` | 1.1.0 | `atlas-all--v1.1.0` | publicada e marcada como latest |

## Checklist concluído

- [x] Versões e changelogs alinhados.
- [x] Testes de contrato e validação do repositório aprovados.
- [x] Auditoria e instalação real dos pacotes aprovadas no CI.
- [x] Aprovação do solicitante registrada nesta tarefa.
- [x] Pull request integrado ao `main`.
- [x] Tags imutáveis e GitHub Releases publicadas no commit integrado.
- [x] Sincronização do kit concluída.

## Histórico

- 2026-09-24 — Pacotes 1.1.0 publicados com suporte aos targets `kiro` e `copilot`, além do gerenciador de APMs.
- 2026-09-23 — Pacotes 1.0.0 publicados como baseline inicial.
