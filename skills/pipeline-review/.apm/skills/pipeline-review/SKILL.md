---
name: pipeline-review
description: Use quando revisar ou diagnosticar pipelines CI/CD, especialmente GitHub Actions, com foco em permissões, segredos, dependências, gatilhos e reprodutibilidade. Produza achados acionáveis sem disparar deploys ou alterar ambientes externos.
---

# Revisão de pipelines

## Fluxo

1. Identifique eventos, atores, dados não confiáveis, ambientes e credenciais alcançados pelo workflow.
2. Modele o caminho de execução por job: checkout, build, teste, pacote, aprovação e deploy.
3. Aplique [references/pipeline-checklist.md](references/pipeline-checklist.md) somente onde houver efeito concreto.
4. Confirme cada achado no YAML e nas regras da plataforma; não presuma defaults sem evidência.
5. Relate severidade, cenário explorável ou de falha e a menor correção.
6. Destaque lacunas que dependem de rulesets, ambientes ou secrets fora do repositório.

## Restrições

- Não execute workflows, deploys, releases ou rotação de secrets.
- Não copie valores de secrets para logs, outputs ou artefatos.
- Não recomende permissão ampla quando uma permissão de job mais estreita resolve.
- Diferencie pin por tag, que pode mover, de pin por SHA imutável.
- Mudança cosmética ou preferência de estilo não é achado de segurança.

