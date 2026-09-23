---
name: terraform-review
description: Use quando revisar uma mudança Terraform, investigar um plano ou preparar feedback de infraestrutura como código. Aplique segurança, confiabilidade, custo e padrões do repositório sem executar apply nem alterar infraestrutura.
---

# Revisão de Terraform

Produza uma revisão acionável e proporcional ao risco da mudança.

## Fluxo

1. Leia as convenções do repositório e delimite arquivos, módulos, ambientes e recursos alterados.
2. Inspecione o diff e, quando disponível, o plano correspondente. Não trate um plano antigo como evidência da revisão atual.
3. Consulte [references/review-checklist.md](references/review-checklist.md) para as categorias aplicáveis.
4. Priorize efeitos concretos: destruição, exposição, indisponibilidade, privilégio, perda de dados, drift e custo relevante.
5. Para cada achado, cite o arquivo e a menor faixa de linhas útil, explique o cenário de falha e proponha a menor correção segura.
6. Diferencie erro bloqueante, risco que exige decisão e sugestão opcional. Se não houver achados, diga isso e registre lacunas de validação.

## Restrições

- Não execute `terraform apply`, importe recursos, destrave state nem mude infraestrutura.
- Não solicite nem exponha credenciais ou conteúdo sensível do state.
- Não presuma que toda diferença de formatação é um defeito funcional.
- Não proponha abstração ampla sem um risco ou duplicação observável.
- Prefira comandos de leitura, `fmt -check`, `validate` e `plan` somente quando o ambiente e as permissões permitirem.

