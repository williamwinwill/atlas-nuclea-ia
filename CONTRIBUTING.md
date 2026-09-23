# Contribuindo

## Nova skill

1. Copie a estrutura de um pacote existente para `skills/<nome-kebab-case>`.
2. Escreva uma descrição de frontmatter que comece pela intenção do usuário e diferencie claramente quando a skill deve ser usada.
3. Comece em `1.0.0`, documente a release no changelog e cadastre o componente no Atlas.
4. Inclua ao menos um cenário positivo e um de limite em `tests/cases.yml`.
5. Rode a validação local e abra uma PR curta.

Uma PR aprovada autoriza o merge; a versão só passa a ser oficial quando o workflow de release conclui.

## Mudança em skill existente

- **Patch:** corrige instrução, exemplo ou script sem mudar o contrato.
- **Minor:** adiciona capacidade compatível.
- **Major:** muda comportamento, entrada, permissão ou dependência e exige adaptação do consumidor.

Atualize `version` e `CHANGELOG.md` na mesma PR. O CI rejeita mudança publicável sem incremento.

## Revisão

O revisor confirma:

- escopo e descrição da skill;
- ausência de segredos, instruções ocultas e execução desnecessária;
- privilégio mínimo para scripts e MCPs;
- cenários comportamentais relevantes;
- SemVer e changelog coerentes;
- impacto sobre kits e consumidores.

## Kit completo

Não edite `kits/all/apm.yml` para antecipar uma skill ainda não publicada. Depois da release individual, `sync-kit.yml` abre uma PR que atualiza o conjunto fechado do kit. Mudança de membros incrementa minor; atualização das mesmas skills incrementa patch.

