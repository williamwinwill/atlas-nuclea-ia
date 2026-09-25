const DEMO_CATALOG = {
  mode: "demo",
  repositoryReady: false,
  defaultTarget: "kiro",
  supportedTargets: ["kiro", "copilot"],
  currentUser: "William Fernandes",
  repositoryUrl: "https://github.com/nuclea/atlas-nuclea-ia",
  apms: [
    {
      id: "all",
      name: "atlas-all",
      description: "Kit completo de skills oficiais do Atlas para jornadas de engenharia.",
      version: "1.0.0",
      kind: "official",
      type: "squad",
      segment: "Atlas",
      author: "Núclea Platform AI",
      requestedBy: "Platform AI",
      updatedAt: "2026-09-24T18:42:00-03:00",
      skillIds: ["pipeline-review", "sonar-fix", "terraform-review"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/all#atlas-all--v1.0.0 --target kiro",
    },
    {
      id: "backend-essentials",
      name: "backend-essentials",
      description: "Pacote enxuto para revisão de pipelines e tratamento de findings do SonarQube.",
      version: "1.2.0",
      kind: "custom",
      type: "squad",
      segment: "CPO",
      author: "Peterson Vieira",
      requestedBy: "Squad Developer Experience",
      updatedAt: "2026-09-23T14:18:00-03:00",
      skillIds: ["pipeline-review", "sonar-fix"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/backend-essentials#backend-essentials--v1.2.0 --target kiro",
    },
    {
      id: "infra-guardrails",
      name: "infra-guardrails",
      description: "Guardrails de infraestrutura como código para revisões consistentes e seguras.",
      version: "1.1.3",
      kind: "custom",
      type: "front",
      segment: "Banco de dados",
      author: "Ana Martins",
      requestedBy: "Cloud Platform",
      updatedAt: "2026-09-22T10:05:00-03:00",
      skillIds: ["terraform-review", "pipeline-review"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/infra-guardrails#infra-guardrails--v1.1.3 --target kiro",
    },
    {
      id: "java-modernization",
      name: "java-modernization",
      description: "Apoio à modernização de serviços Java, revisão de APIs e qualidade contínua.",
      version: "2.3.0",
      kind: "custom",
      type: "front",
      segment: "Engenharia Java",
      author: "Mariana Costa",
      requestedBy: "Chapter Backend",
      updatedAt: "2026-09-21T16:30:00-03:00",
      skillIds: ["java-modernization", "api-review", "sonar-fix"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/java-modernization#java-modernization--v2.3.0 --target kiro",
    },
    {
      id: "web-experience",
      name: "web-experience",
      description: "Boas práticas de frontend, acessibilidade e documentação para produtos web.",
      version: "1.4.2",
      kind: "custom",
      type: "front",
      segment: "Experiência Web",
      author: "Rafael Lima",
      requestedBy: "Design System",
      updatedAt: "2026-09-20T11:12:00-03:00",
      skillIds: ["web-accessibility", "documentation", "api-review"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/web-experience#web-experience--v1.4.2 --target kiro",
    },
    {
      id: "qa-release",
      name: "qa-release",
      description: "Planejamento de testes e gates automatizados para jornadas críticas de release.",
      version: "1.6.0",
      kind: "custom",
      type: "front",
      segment: "Qualidade e Confiabilidade",
      author: "Beatriz Rocha",
      requestedBy: "Quality Engineering",
      updatedAt: "2026-09-19T09:44:00-03:00",
      skillIds: ["qa-test-plan", "pipeline-review", "observability"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/qa-release#qa-release--v1.6.0 --target kiro",
    },
    {
      id: "data-foundation",
      name: "data-foundation",
      description: "Padrões de banco de dados, performance e observabilidade para plataformas de dados.",
      version: "0.9.4",
      kind: "custom",
      type: "front",
      segment: "Data Platform",
      author: "Lucas Alves",
      requestedBy: "Dados & Analytics",
      updatedAt: "2026-09-18T15:06:00-03:00",
      skillIds: ["database-performance", "observability", "terraform-review"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/data-foundation#data-foundation--v0.9.4 --target kiro",
    },
    {
      id: "ctc-secure-delivery",
      name: "ctc-secure-delivery",
      description: "Guardrails de segurança, qualidade e entrega contínua para a squad CTC.",
      version: "1.8.1",
      kind: "custom",
      type: "squad",
      segment: "CTC Pagamentos",
      author: "Camila Souza",
      requestedBy: "CTC",
      updatedAt: "2026-09-17T13:25:00-03:00",
      skillIds: ["security-review", "pipeline-review", "sonar-fix"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/ctc-secure-delivery#ctc-secure-delivery--v1.8.1 --target kiro",
    },
    {
      id: "cpo-product-discovery",
      name: "cpo-product-discovery",
      description: "Documentação, contratos de API e padrões de engenharia para a frente de produto.",
      version: "1.0.5",
      kind: "custom",
      type: "squad",
      segment: "CPO Open Finance",
      author: "Fernanda Melo",
      requestedBy: "CPO",
      updatedAt: "2026-09-16T10:40:00-03:00",
      skillIds: ["documentation", "api-review", "git-commit"],
      command:
        "apm install nuclea/atlas-nuclea-ia/kits/cpo-product-discovery#cpo-product-discovery--v1.0.5 --target kiro",
    },
  ],
  skills: [
    {
      id: "pipeline-review",
      name: "Pipeline Review",
      description: "Revisão especializada de pipelines CI/CD.",
      version: "1.0.0",
    },
    {
      id: "sonar-fix",
      name: "Sonar Fix",
      description: "Diagnóstico e correção local de findings do SonarQube.",
      version: "1.0.0",
    },
    {
      id: "terraform-review",
      name: "Terraform Review",
      description: "Revisão de módulos e planos Terraform com foco em segurança.",
      version: "1.0.0",
    },
    {
      id: "git-commit",
      name: "Git Commit",
      description: "Commits semânticos e padronizados a partir do diff.",
      version: "1.0.0",
    },
    {
      id: "api-review",
      name: "API Review",
      description: "Revisão de contratos REST, eventos e compatibilidade.",
      version: "0.8.0",
    },
    {
      id: "documentation",
      name: "Documentation",
      description: "Criação e manutenção de documentação técnica.",
      version: "1.3.1",
    },
    {
      id: "java-modernization",
      name: "Java Modernization",
      description: "Modernização segura de aplicações Java e atualização de dependências.",
      version: "1.1.0",
    },
    {
      id: "web-accessibility",
      name: "Web Accessibility",
      description: "Revisão de acessibilidade, semântica e navegação por teclado.",
      version: "1.0.2",
    },
    {
      id: "qa-test-plan",
      name: "QA Test Plan",
      description: "Estratégias de testes funcionais, integração e regressão.",
      version: "1.2.0",
    },
    {
      id: "database-performance",
      name: "Database Performance",
      description: "Análise de queries, índices e capacidade de bancos de dados.",
      version: "0.9.1",
    },
    {
      id: "observability",
      name: "Observability",
      description: "Padrões de métricas, logs, traces e alertas acionáveis.",
      version: "1.4.0",
    },
    {
      id: "security-review",
      name: "Security Review",
      description: "Revisão de riscos, segredos e controles de segurança.",
      version: "1.3.0",
    },
  ],
};

const TARGETS = {
  kiro: "Kiro",
  copilot: "GitHub Copilot",
};

DEMO_CATALOG.skills.forEach((skill) => {
  skill.targets = ["kiro", "copilot"];
});
DEMO_CATALOG.apms.forEach((apm, index) => {
  apm.targets = index % 3 === 0 ? ["kiro", "copilot"] : ["kiro"];
});

const accents = ["#b7ef43", "#54d5ff", "#a691ff", "#ffae66", "#66e0bd", "#ff8bb4"];
const APM_TYPES = {
  squad: {
    label: "Squad",
    placeholder: "ex.: CTC Pagamentos",
    suggestions: ["CPO", "CTC", "Atlas", "CPO Open Finance", "CTC Pagamentos"],
  },
  front: {
    label: "Frente",
    placeholder: "ex.: Engenharia Java",
    suggestions: [
      "Banco de dados",
      "Desenvolvimento web",
      "Engenharia Java",
      "Qualidade e Confiabilidade",
    ],
  },
};

const state = {
  catalog: structuredClone(DEMO_CATALOG),
  filter: "all",
  query: "",
  mode: "edit",
  currentApm: null,
  selectedTargetIds: new Set(["kiro"]),
  selectedSkillIds: new Set(),
  originalSkillIds: new Set(),
  markedAvailable: new Set(),
  markedSelected: new Set(),
  availableQuery: "",
  selectedQuery: "",
  saving: false,
  touched: new Set(),
  syncResetTimer: null,
};

const elements = {
  grid: document.querySelector("#card-grid"),
  empty: document.querySelector("#empty-state"),
  pageCount: document.querySelector("#page-count"),
  resultCount: document.querySelector("#result-count"),
  currentUser: document.querySelector("#current-user"),
  catalogSearch: document.querySelector("#catalog-search"),
  createButton: document.querySelector("#create-button"),
  refreshButton: document.querySelector("#refresh-button"),
  syncStatus: document.querySelector("#sync-status"),
  syncCopy: document.querySelector("#sync-copy"),
  dialog: document.querySelector("#apm-dialog"),
  form: document.querySelector("#apm-form"),
  dialogKicker: document.querySelector("#dialog-kicker"),
  dialogTitle: document.querySelector("#dialog-title"),
  closeDialog: document.querySelector("#close-dialog"),
  cancelButton: document.querySelector("#cancel-button"),
  createFields: document.querySelector("#create-fields"),
  nameInput: document.querySelector("#apm-name"),
  descriptionInput: document.querySelector("#apm-description"),
  typeInput: document.querySelector("#apm-type"),
  segmentInput: document.querySelector("#apm-segment"),
  segmentSuggestions: document.querySelector("#segment-suggestions"),
  segmentLabel: document.querySelector("#segment-label"),
  segmentHelp: document.querySelector("#segment-help"),
  targetInputs: [...document.querySelectorAll('input[name="targets"]')],
  requirements: [...document.querySelectorAll("[data-requirement]")],
  detailGrid: document.querySelector("#detail-grid"),
  detailAuthor: document.querySelector("#detail-author"),
  detailDate: document.querySelector("#detail-date"),
  detailVersion: document.querySelector("#detail-version"),
  detailCommand: document.querySelector("#detail-command"),
  detailTarget: document.querySelector("#detail-target"),
  copyCommand: document.querySelector("#copy-command"),
  availableSearch: document.querySelector("#available-search"),
  selectedSearch: document.querySelector("#selected-search"),
  availableList: document.querySelector("#available-list"),
  selectedList: document.querySelector("#selected-list"),
  availableCount: document.querySelector("#available-count"),
  selectedCount: document.querySelector("#selected-count"),
  addSelected: document.querySelector("#add-selected"),
  removeSelected: document.querySelector("#remove-selected"),
  addAll: document.querySelector("#add-all"),
  removeAll: document.querySelector("#remove-all"),
  changeIndicator: document.querySelector("#change-indicator"),
  changeCopy: document.querySelector("#change-copy"),
  saveButton: document.querySelector("#save-button"),
  saveLabel: document.querySelector("#save-button .button-label"),
  saveError: document.querySelector("#save-error"),
  saveErrorCopy: document.querySelector("#save-error-copy"),
  toastRegion: document.querySelector("#toast-region"),
};

function withMockExamples(catalog) {
  const skillIds = new Set(catalog.skills.map((skill) => skill.id));
  const apmIds = new Set(catalog.apms.map((apm) => apm.id));
  const mockSkills = DEMO_CATALOG.skills
    .filter((skill) => !skillIds.has(skill.id))
    .map((skill) => ({ ...skill, isMock: true }));
  const mockApms = DEMO_CATALOG.apms
    .filter((apm) => !apmIds.has(apm.id))
    .map((apm) => ({ ...apm, isMock: true }));
  return {
    ...catalog,
    skills: [...catalog.skills, ...mockSkills],
    apms: [...catalog.apms, ...mockApms],
  };
}

function setSyncState(syncState, copy) {
  window.clearTimeout(state.syncResetTimer);
  elements.syncStatus.dataset.state = syncState;
  elements.syncCopy.textContent = copy;
  if (syncState === "updated") {
    state.syncResetTimer = window.setTimeout(() => {
      elements.syncStatus.dataset.state = "synced";
      elements.syncCopy.textContent =
        state.catalog.repositoryReady === false ? "Modo demonstração" : "Sincronizado com o repositório";
    }, 3200);
  }
}

async function fetchCatalog({ announceFallback = false, withFeedback = false } = {}) {
  const startedAt = performance.now();
  elements.refreshButton.disabled = true;
  elements.syncStatus.disabled = true;
  if (withFeedback) setSyncState("syncing", "Sincronizando com o repositório…");
  try {
    const response = await fetch("/api/catalog", { headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(`Catálogo indisponível (${response.status})`);
    const catalog = await response.json();
    state.catalog = { mode: "connected", ...withMockExamples(catalog) };
    const isPreview = catalog.repositoryReady === false;
    if (withFeedback) {
      const remaining = Math.max(0, 700 - (performance.now() - startedAt));
      await new Promise((resolve) => window.setTimeout(resolve, remaining));
      setSyncState("updated", isPreview ? "Prévia atualizada agora" : "Catálogo atualizado agora");
    } else {
      setSyncState("synced", isPreview ? "Modo demonstração" : "Sincronizado com o repositório");
    }
  } catch (error) {
    if (state.catalog.mode !== "connected") {
      state.catalog = structuredClone(DEMO_CATALOG);
      setSyncState(
        announceFallback ? "error" : "synced",
        announceFallback ? "Não foi possível sincronizar" : "Prévia local",
      );
    } else {
      setSyncState("error", "Não foi possível sincronizar");
    }
    if (announceFallback) {
      showToast("Backend indisponível. Exibindo dados de demonstração.", "error");
    }
  } finally {
    elements.refreshButton.disabled = false;
    elements.syncStatus.disabled = false;
    renderCatalog();
  }
}

function normalize(value) {
  return String(value ?? "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value) {
  if (!value) return "Data não disponível";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function skillById(id) {
  return state.catalog.skills.find((skill) => skill.id === id);
}

function targetLabel(target) {
  return TARGETS[target] || target;
}

function skillTargets(skill) {
  return Array.isArray(skill.targets) && skill.targets.length ? skill.targets : ["kiro"];
}

function missingSkillTargets(skill) {
  const supported = new Set(skillTargets(skill));
  return [...state.selectedTargetIds].filter((target) => !supported.has(target));
}

function skillsAreCompatible() {
  return [...state.selectedSkillIds].every((skillId) => {
    const skill = skillById(skillId);
    return skill && missingSkillTargets(skill).length === 0;
  });
}

function commandForTarget(command, target) {
  return command.replace(/--target\s+\S+/, `--target ${target}`);
}

function apmType(apm) {
  return apm.type || (apm.kind === "official" ? "squad" : "front");
}

function apmSegment(apm) {
  if (apm.segment) return apm.segment;
  return apmType(apm) === "squad" ? "Atlas" : "Desenvolvimento web";
}

function filteredApms() {
  const query = normalize(state.query);
  return state.catalog.apms.filter((apm) => {
    const type = apmType(apm);
    const matchesFilter = state.filter === "all" || type === state.filter;
    const haystack = normalize(
      `${apm.name} ${apm.description} ${apm.author} ${apm.requestedBy} ${type} ${apmSegment(apm)}`,
    );
    return matchesFilter && (!query || haystack.includes(query));
  });
}

function renderCatalog() {
  const apms = filteredApms();
  elements.pageCount.textContent = `${state.catalog.apms.length} ${state.catalog.apms.length === 1 ? "pacote" : "pacotes"}`;
  elements.resultCount.textContent = String(apms.length);
  elements.currentUser.textContent = state.catalog.currentUser || "Usuário do Git";
  elements.empty.hidden = apms.length > 0;
  elements.grid.hidden = apms.length === 0;

  elements.grid.innerHTML = apms
    .map((apm, index) => {
      const skills = apm.skillIds.map(skillById).filter(Boolean);
      const visibleSkills = skills.slice(0, 2);
      const remaining = Math.max(0, skills.length - visibleSkills.length);
      const accent = accents[index % accents.length];
      const type = apmType(apm);
      const typeLabel = APM_TYPES[type]?.label || "APM";
      return `
        <article
          class="apm-card"
          role="button"
          tabindex="0"
          data-apm-id="${escapeHtml(apm.id)}"
          style="--accent: ${accent}; --accent-soft: color-mix(in srgb, ${accent} 16%, transparent)"
          aria-label="Abrir detalhes do APM ${escapeHtml(apm.name)}"
        >
          <div class="card-top">
            <div class="card-identity">
              <span class="card-icon" aria-hidden="true">${escapeHtml(apm.name.slice(0, 1).toUpperCase())}</span>
              <div class="card-title">
                <h3>${escapeHtml(apm.name)}</h3>
                <span class="version-badge">v${escapeHtml(apm.version)}</span>
              </div>
            </div>
            <span class="type-badge">${escapeHtml(typeLabel)} · ${escapeHtml(apmSegment(apm))}</span>
          </div>
          <p class="card-description">${escapeHtml(apm.description)}</p>
          <div class="card-targets" aria-label="Targets compatíveis">
            ${(apm.targets || ["kiro"])
              .map((target) => `<span class="card-target">${escapeHtml(targetLabel(target))}</span>`)
              .join("")}
          </div>
          <div class="skill-chips" aria-label="${skills.length} skills adicionadas">
            ${visibleSkills.map((skill) => `<span class="skill-chip">${escapeHtml(skill.name)}</span>`).join("")}
            ${remaining ? `<span class="skill-chip more">+${remaining}</span>` : ""}
          </div>
          <footer class="card-meta">
            <span>
              <small>Última alteração</small>
              <strong>${escapeHtml(apm.author || "Não informado")}</strong>
            </span>
            <span>
              <small>Atualizado em</small>
              <strong>${escapeHtml(formatDate(apm.updatedAt))}</strong>
            </span>
          </footer>
        </article>
      `;
    })
    .join("");
}

function openApm(apmId) {
  const apm = state.catalog.apms.find((item) => item.id === apmId);
  if (!apm) return;
  state.mode = "edit";
  state.currentApm = apm;
  state.selectedTargetIds = new Set(apm.targets || [state.catalog.defaultTarget || "kiro"]);
  state.selectedSkillIds = new Set(apm.skillIds);
  state.originalSkillIds = new Set(apm.skillIds);
  state.touched = new Set();
  resetDialogSelection();

  elements.dialogKicker.textContent = "DETALHE DO APM";
  elements.dialogTitle.textContent = apm.name;
  elements.createFields.hidden = true;
  elements.detailGrid.hidden = false;
  elements.detailAuthor.textContent = apm.author || apm.requestedBy || "Não informado";
  elements.detailDate.textContent = formatDate(apm.updatedAt);
  elements.detailVersion.textContent = `v${apm.version}`;
  elements.detailTarget.innerHTML = [...state.selectedTargetIds]
    .map((target) => `<option value="${escapeHtml(target)}">${escapeHtml(targetLabel(target))}</option>`)
    .join("");
  const commandTarget = state.selectedTargetIds.has(state.catalog.defaultTarget)
    ? state.catalog.defaultTarget
    : [...state.selectedTargetIds][0];
  elements.detailTarget.value = commandTarget;
  elements.detailCommand.textContent = commandForTarget(apm.command, commandTarget);
  clearSaveError();
  renderDualList();
  updateDirtyState();
  elements.dialog.showModal();
}

function openCreate() {
  state.mode = "create";
  state.currentApm = null;
  state.selectedTargetIds = new Set([state.catalog.defaultTarget || "kiro"]);
  state.selectedSkillIds = new Set();
  state.originalSkillIds = new Set();
  state.touched = new Set();
  resetDialogSelection();

  elements.dialogKicker.textContent = "NOVO PACOTE";
  elements.dialogTitle.textContent = "Criar APM";
  elements.createFields.hidden = false;
  elements.detailGrid.hidden = true;
  elements.nameInput.value = "";
  elements.descriptionInput.value = "";
  elements.typeInput.value = "";
  populateSegments("");
  elements.targetInputs.forEach((input) => {
    input.checked = state.selectedTargetIds.has(input.value);
  });
  clearSaveError();
  renderDualList();
  updateDirtyState();
  elements.dialog.showModal();
  window.setTimeout(() => elements.nameInput.focus(), 0);
}

function populateSegments(type, selectedValue = "") {
  const config = APM_TYPES[type];
  elements.segmentInput.disabled = !config;
  elements.segmentLabel.textContent = config ? config.label : "Squad ou frente";
  elements.segmentHelp.textContent = config
    ? `Digite livremente ${config.label === "Squad" ? "a squad" : "a frente técnica"} responsável pelo pacote.`
    : "Selecione primeiro o tipo de APM.";
  elements.segmentInput.placeholder = config ? config.placeholder : "Escolha primeiro o tipo";
  elements.segmentSuggestions.innerHTML = config
    ? config.suggestions.map((suggestion) => `<option value="${escapeHtml(suggestion)}"></option>`).join("")
    : "";
  elements.segmentInput.value = selectedValue;
}

function clearSaveError() {
  elements.saveError.hidden = true;
  elements.saveErrorCopy.textContent = "";
}

function showSaveError(message) {
  elements.saveErrorCopy.textContent = message;
  elements.saveError.hidden = false;
  elements.saveError.focus({ preventScroll: true });
}

function resetDialogSelection() {
  state.markedAvailable = new Set();
  state.markedSelected = new Set();
  state.availableQuery = "";
  state.selectedQuery = "";
  elements.availableSearch.value = "";
  elements.selectedSearch.value = "";
}

function skillMatches(skill, query) {
  const normalized = normalize(query);
  return !normalized || normalize(`${skill.name} ${skill.description} ${skill.id}`).includes(normalized);
}

function renderSkillOptions(skills, markedIds, side) {
  if (!skills.length) {
    return `<div class="list-empty">${side === "available" ? "Nenhuma skill disponível para esta busca." : "Nenhuma skill adicionada ao pacote."}</div>`;
  }
  return skills
    .map((skill) => {
      const missingTargets = missingSkillTargets(skill);
      const incompatible = missingTargets.length > 0;
      const disabled = side === "available" && incompatible;
      return `
        <button
          class="skill-option${incompatible ? " incompatible" : ""}"
          type="button"
          role="option"
          aria-selected="${markedIds.has(skill.id)}"
          data-skill-id="${escapeHtml(skill.id)}"
          data-side="${side}"
          ${disabled ? "disabled" : ""}
        >
          <span class="option-check" aria-hidden="true">✓</span>
          <span class="option-copy">
            <strong>${escapeHtml(skill.name)}</strong>
            <small>${escapeHtml(skill.description)}</small>
            <span class="option-targets">
              ${skillTargets(skill)
                .map((target) => `<span class="option-target">${escapeHtml(targetLabel(target))}</span>`)
                .join("")}
            </span>
            ${incompatible ? `<span class="option-warning">Falta ${escapeHtml(missingTargets.map(targetLabel).join(" e "))}</span>` : ""}
          </span>
          <span class="option-version">v${escapeHtml(skill.version)}</span>
        </button>
      `;
    })
    .join("");
}

function renderDualList() {
  const available = state.catalog.skills.filter(
    (skill) => !state.selectedSkillIds.has(skill.id) && skillMatches(skill, state.availableQuery),
  );
  const selected = state.catalog.skills.filter(
    (skill) => state.selectedSkillIds.has(skill.id) && skillMatches(skill, state.selectedQuery),
  );
  const totalAvailable = state.catalog.skills.length - state.selectedSkillIds.size;
  const totalSelected = state.selectedSkillIds.size;

  elements.availableList.innerHTML = renderSkillOptions(available, state.markedAvailable, "available");
  elements.selectedList.innerHTML = renderSkillOptions(selected, state.markedSelected, "selected");
  elements.availableCount.textContent = `${totalAvailable} ${totalAvailable === 1 ? "skill" : "skills"}`;
  elements.selectedCount.textContent = `${totalSelected} ${totalSelected === 1 ? "skill" : "skills"}`;
  elements.addSelected.disabled = state.markedAvailable.size === 0;
  elements.removeSelected.disabled = state.markedSelected.size === 0;
  elements.addAll.disabled = !available.some((skill) => missingSkillTargets(skill).length === 0);
  elements.removeAll.disabled = totalSelected === 0;
}

function toggleMarked(side, skillId) {
  const target = side === "available" ? state.markedAvailable : state.markedSelected;
  target.has(skillId) ? target.delete(skillId) : target.add(skillId);
  renderDualList();
}

function transferMarked(direction) {
  const adding = direction === "add";
  const source = adding ? state.markedAvailable : state.markedSelected;
  source.forEach((skillId) => {
    const skill = skillById(skillId);
    if (adding && skill && missingSkillTargets(skill).length === 0) {
      state.selectedSkillIds.add(skillId);
    } else if (!adding) {
      state.selectedSkillIds.delete(skillId);
    }
  });
  source.clear();
  clearSaveError();
  renderDualList();
  updateDirtyState();
}

function transferAll(direction) {
  if (direction === "add") {
    state.catalog.skills
      .filter(
        (skill) =>
          !state.selectedSkillIds.has(skill.id) &&
          skillMatches(skill, state.availableQuery) &&
          missingSkillTargets(skill).length === 0,
      )
      .forEach((skill) => state.selectedSkillIds.add(skill.id));
  } else {
    state.catalog.skills
      .filter((skill) => state.selectedSkillIds.has(skill.id) && skillMatches(skill, state.selectedQuery))
      .forEach((skill) => state.selectedSkillIds.delete(skill.id));
  }
  state.markedAvailable.clear();
  state.markedSelected.clear();
  clearSaveError();
  renderDualList();
  updateDirtyState();
}

function setsEqual(a, b) {
  return a.size === b.size && [...a].every((item) => b.has(item));
}

function createChecks() {
  const type = elements.typeInput.value;
  const segment = elements.segmentInput.value.trim();
  return {
    name: /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(elements.nameInput.value.trim()),
    description: elements.descriptionInput.value.trim().length >= 8,
    type: Boolean(APM_TYPES[type]),
    segment: segment.length >= 2 && segment.length <= 60,
    targets: state.selectedTargetIds.size > 0,
    skills: state.selectedSkillIds.size > 0,
    compatibility: state.selectedSkillIds.size === 0 || skillsAreCompatible(),
  };
}

function isCreateValid() {
  return Object.values(createChecks()).every(Boolean);
}

function isDirty() {
  return state.mode === "create"
    ? isCreateValid()
    : !setsEqual(state.selectedSkillIds, state.originalSkillIds) && skillsAreCompatible();
}

function updateDirtyState() {
  const dirty = isDirty();
  elements.changeIndicator.classList.toggle("dirty", dirty);
  if (state.mode === "create") {
    const checks = createChecks();
    elements.requirements.forEach((requirement) => {
      requirement.classList.toggle("complete", checks[requirement.dataset.requirement]);
    });
    const missingLabels = {
      name: "nome válido",
      description: "descrição",
      type: "tipo",
      segment: "squad ou frente",
      targets: "ao menos um target",
      skills: "ao menos uma skill",
      compatibility: "skills compatíveis com os targets",
    };
    const missing = Object.entries(checks)
      .filter(([, complete]) => !complete)
      .map(([key]) => missingLabels[key]);
    elements.changeCopy.textContent = missing.length
      ? `Falta preencher: ${missing.join(", ")}`
      : "APM pronto para salvar";

    const fields = {
      name: elements.nameInput,
      description: elements.descriptionInput,
      type: elements.typeInput,
      segment: elements.segmentInput,
    };
    Object.entries(fields).forEach(([key, field]) => {
      field.classList.toggle("invalid", state.touched.has(key) && !checks[key]);
    });
  } else {
    const changed = !setsEqual(state.selectedSkillIds, state.originalSkillIds);
    elements.changeCopy.textContent = !skillsAreCompatible()
      ? "Há skills incompatíveis com os targets do APM"
      : changed
        ? "Alterações prontas para salvar"
        : "Nenhuma alteração pendente";
  }
  elements.saveButton.disabled = !dirty || state.saving;
}

function closeDialog() {
  elements.dialog.close();
}

async function saveApm() {
  if (!isDirty() || state.saving) return;
  clearSaveError();
  state.saving = true;
  elements.saveButton.disabled = true;
  elements.saveButton.classList.add("loading");
  elements.saveLabel.textContent = "Salvando APM…";
  elements.cancelButton.disabled = true;
  elements.closeDialog.disabled = true;
  setSyncState("syncing", "Salvando e sincronizando…");

  const isCreate = state.mode === "create";
  const payload = {
    skillIds: [...state.selectedSkillIds],
    requestedBy: state.catalog.currentUser,
  };
  if (isCreate) {
    payload.name = elements.nameInput.value.trim();
    payload.description = elements.descriptionInput.value.trim();
    payload.apmType = elements.typeInput.value;
    payload.segment = elements.segmentInput.value.trim();
    payload.targets = [...state.selectedTargetIds];
  }

  try {
    const shouldSimulate =
      state.catalog.mode === "demo" ||
      state.catalog.repositoryReady === false ||
      state.currentApm?.isMock === true;
    if (shouldSimulate) {
      await new Promise((resolve) => window.setTimeout(resolve, 650));
      applyDemoSave(payload);
      showToast("APM salvo na demonstração.");
    } else {
      const endpoint = isCreate ? "/api/apms" : `/api/apms/${encodeURIComponent(state.currentApm.id)}`;
      const response = await fetch(endpoint, {
        method: isCreate ? "POST" : "PUT",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.error || `Falha ao salvar (${response.status})`);
      if (result.pushed === false) {
        showToast("APM salvo. A sincronização com o repositório ficou pendente.", "error");
      } else {
        showToast("APM atualizado no repositório.");
      }
      await fetchCatalog();
    }
    setSyncState("updated", "APM atualizado agora");
    closeDialog();
    renderCatalog();
  } catch (error) {
    setSyncState("error", "Falha ao atualizar o APM");
    const message = error.message || "Não foi possível salvar o APM.";
    showSaveError(message);
    showToast(message, "error");
  } finally {
    state.saving = false;
    elements.saveButton.classList.remove("loading");
    elements.saveLabel.textContent = "Salvar APM";
    elements.cancelButton.disabled = false;
    elements.closeDialog.disabled = false;
    updateDirtyState();
  }
}

function applyDemoSave(payload) {
  if (state.mode === "create") {
    const newApm = {
      id: payload.name,
      name: payload.name,
      description: payload.description,
      version: "1.0.0",
      kind: "custom",
      type: payload.apmType,
      segment: payload.segment,
      targets: payload.targets,
      isMock: true,
      author: payload.requestedBy,
      requestedBy: payload.requestedBy,
      updatedAt: new Date().toISOString(),
      skillIds: payload.skillIds,
      command: `apm install nuclea/atlas-nuclea-ia/kits/${payload.name}#${payload.name}--v1.0.0 --target ${payload.targets[0]}`,
    };
    state.catalog.apms.unshift(newApm);
  } else {
    state.currentApm.skillIds = payload.skillIds;
    state.currentApm.version = bumpPatch(state.currentApm.version);
    state.currentApm.author = payload.requestedBy;
    state.currentApm.updatedAt = new Date().toISOString();
    state.currentApm.command = state.currentApm.command.replace(
      /--v[^\s]+/,
      `--v${state.currentApm.version}`,
    );
  }
}

function bumpPatch(version) {
  const [major, minor, patch] = version.split(".").map(Number);
  return `${major}.${minor}.${patch + 1}`;
}

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon" aria-hidden="true">${type === "error" ? "!" : "✓"}</span>
    <span>${escapeHtml(message)}</span>
    <button type="button" aria-label="Fechar notificação">×</button>
  `;
  const remove = () => {
    toast.dataset.state = "leaving";
    window.setTimeout(() => toast.remove(), 200);
  };
  toast.querySelector("button").addEventListener("click", remove);
  elements.toastRegion.append(toast);
  window.setTimeout(remove, 4500);
}

document.querySelectorAll(".filter-chip").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filter-chip").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    state.filter = button.dataset.filter;
    renderCatalog();
  });
});

elements.catalogSearch.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderCatalog();
});

elements.grid.addEventListener("click", (event) => {
  const card = event.target.closest("[data-apm-id]");
  if (card) openApm(card.dataset.apmId);
});

elements.grid.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" && event.key !== " ") return;
  const card = event.target.closest("[data-apm-id]");
  if (!card) return;
  event.preventDefault();
  openApm(card.dataset.apmId);
});

elements.createButton.addEventListener("click", openCreate);
elements.refreshButton.addEventListener("click", () =>
  fetchCatalog({ announceFallback: true, withFeedback: true }),
);
elements.syncStatus.addEventListener("click", () =>
  fetchCatalog({ announceFallback: true, withFeedback: true }),
);
elements.closeDialog.addEventListener("click", () => closeDialog());
elements.cancelButton.addEventListener("click", () => closeDialog());
elements.dialog.addEventListener("cancel", (event) => {
  event.preventDefault();
  closeDialog();
});

elements.availableSearch.addEventListener("input", (event) => {
  state.availableQuery = event.target.value;
  renderDualList();
});

elements.selectedSearch.addEventListener("input", (event) => {
  state.selectedQuery = event.target.value;
  renderDualList();
});

[
  [elements.nameInput, "name"],
  [elements.descriptionInput, "description"],
  [elements.segmentInput, "segment"],
].forEach(([input, key]) => {
  input.addEventListener("input", () => {
    state.touched.add(key);
    clearSaveError();
    updateDirtyState();
  });
});

elements.typeInput.addEventListener("change", () => {
  state.touched.add("type");
  state.touched.delete("segment");
  clearSaveError();
  populateSegments(elements.typeInput.value);
  updateDirtyState();
});

elements.targetInputs.forEach((input) => {
  input.addEventListener("change", () => {
    state.selectedTargetIds = new Set(
      elements.targetInputs.filter((targetInput) => targetInput.checked).map((targetInput) => targetInput.value),
    );
    state.markedAvailable.clear();
    clearSaveError();
    renderDualList();
    updateDirtyState();
  });
});

[elements.availableList, elements.selectedList].forEach((list) => {
  list.addEventListener("click", (event) => {
    const option = event.target.closest("[data-skill-id]");
    if (option) toggleMarked(option.dataset.side, option.dataset.skillId);
  });
  list.addEventListener("dblclick", (event) => {
    const option = event.target.closest("[data-skill-id]");
    if (!option) return;
    const skillId = option.dataset.skillId;
    if (option.dataset.side === "available") {
      state.selectedSkillIds.add(skillId);
      state.markedAvailable.delete(skillId);
    } else {
      state.selectedSkillIds.delete(skillId);
      state.markedSelected.delete(skillId);
    }
    clearSaveError();
    renderDualList();
    updateDirtyState();
  });
});

elements.addSelected.addEventListener("click", () => transferMarked("add"));
elements.removeSelected.addEventListener("click", () => transferMarked("remove"));
elements.addAll.addEventListener("click", () => transferAll("add"));
elements.removeAll.addEventListener("click", () => transferAll("remove"));

elements.copyCommand.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(elements.detailCommand.textContent);
    elements.copyCommand.textContent = "Copiado";
    window.setTimeout(() => (elements.copyCommand.textContent = "Copiar"), 1500);
  } catch {
    showToast("Não foi possível copiar o comando.", "error");
  }
});

elements.detailTarget.addEventListener("change", () => {
  if (!state.currentApm) return;
  elements.detailCommand.textContent = commandForTarget(state.currentApm.command, elements.detailTarget.value);
});

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  saveApm();
});

document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    elements.catalogSearch.focus();
  }
});

fetchCatalog();
