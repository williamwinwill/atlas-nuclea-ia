# Exemplo consumidor: Kiro + SonarQube

O `apm.yml` mostra a forma revisável de instalar o kit completo e ativar o MCP do SonarQube explicitamente.

## Antes de usar

1. Troque a ref humana do kit pelo SHA completo de 40 caracteres registrado na release aprovada. A tag permanece neste exemplo apenas para torná-lo legível e executável após a primeira publicação.
2. Ajuste a URL e o `projectKey` pelo ambiente.
3. Confirme que a versão da imagem SonarQube MCP foi homologada pela plataforma.
4. Use um **user token** com o menor escopo aplicável; não use token de análise do projeto para esse setup.

```bash
export SONARQUBE_TOKEN='...'
export SONARQUBE_URL='https://sonar.example.internal'
export SONARQUBE_PROJECT_KEY='example-service'
apm install
```

O token não deve aparecer no manifesto, lockfile, arquivos gerados ou logs. `SONARQUBE_READ_ONLY=true` impede mudanças de estado no SonarQube, mas a skill ainda pode orientar o Kiro a editar e testar o código local.

Para um MCP compartilhado, substitua `stdio` por um endpoint HTTPS administrado pela plataforma e injete `Authorization: Bearer ${SONARQUBE_TOKEN}` nos headers. Mantenha autenticação individual e TLS; não distribua um token comum.

