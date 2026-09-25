# Arquitetura

## Princípios

O Atlas é a porta de entrada do usuário: apresenta recursos aprovados e abre PRs de adesão ou atualização. O APM instala, resolve, trava e entrega os artefatos ao Kiro. O Kiro executa as skills, acessa MCPs autorizados e edita o código local.

```text
Atlas -> PR revisada -> atlas-nuclea-ia -> tag/release imutável
  |                                             |
  +---- PR no projeto consumidor <--------------+
                      |
                  apm install
                      |
       .kiro/skills + .kiro/settings/mcp.json
```

## Pacotes independentes

Cada diretório imediato sob `skills/` é um pacote APM. A independência permite que `terraform-review` evolua sem alterar a versão de `sonar-fix`. A pasta interna `.apm/skills/<nome>` segue a convenção nativa do APM.

`includes` é uma lista de consentimento para publicação e empacotamento. Ela não é um filtro completo de descoberta na instalação; por isso, somente conteúdo publicável deve ficar dentro de `.apm/`.

## Kits

Um kit é um pacote sem cópia de conteúdo. Seu `apm.yml` depende das releases individuais. `kits/all` representa um conjunto fechado e reproduzível:

- `atlas-all 1.0.0` sempre instala o mesmo conjunto;
- nova skill gera minor do kit;
- nova versão de uma skill já presente gera patch do kit;
- remoção ou mudança incompatível do conjunto exige major.

Quando existirem diferenças reais entre públicos, podem ser criados `kits/devops` e `kits/backend`, reutilizando os mesmos pacotes.

## Modelo de release

Tags Git apontam para o commit inteiro. A identidade da release resulta de `tag + path do pacote`:

| Pacote | Versão | Tag |
|---|---:|---|
| terraform-review | 1.1.0 | `terraform-review--v1.1.0` |
| sonar-fix | 1.1.0 | `sonar-fix--v1.1.0` |
| atlas-all | 1.1.0 | `atlas-all--v1.1.0` |

A tag publicada nunca é movida. O consumidor corporativo usa o caminho do pacote e o SHA completo aprovado. A tag continua como identidade humana no catálogo e nos metadados de release.

## SonarQube

O recurso “Sonar: consultar e corrigir problemas” tem quatro partes:

| Componente | Responsabilidade |
|---|---|
| MCP do SonarQube | Consultar issues, regras, medidas e Quality Gate |
| `sonar-fix` | Conduzir diagnóstico, correção e validação |
| Kiro | Ler/editar arquivos locais e executar testes |
| Pipeline | Rodar a análise oficial e confirmar o resultado |

`SONARQUBE_READ_ONLY=true` impede que o MCP mude o estado no Sonar. Isso não impede que o Kiro corrija o código local. A credencial é um user token fornecido no ambiente e nunca entra no Git.

MCPs transitivos não são ativados implicitamente. O Atlas inclui `dependencies.mcp` diretamente no manifesto raiz do consumidor, onde a alteração pode ser revisada.
