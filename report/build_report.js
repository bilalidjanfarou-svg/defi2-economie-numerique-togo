const pptxgen = require("pptxgenjs");

const COLOR = {
  navy: "12203C",
  navyLight: "1C3057",
  teal: "17A2B8",
  amber: "F4A100",
  white: "FFFFFF",
  offwhite: "F4F6F9",
  gray: "6B7684",
  darkText: "1A1A1A",
};

const FONT_HEAD = "Cambria";
const FONT_BODY = "Calibri";

let pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5

function bg(slide, color) {
  slide.background = { color };
}

// ---------------------------------------------------------------------------
// Slide 1 — Titre
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.navy);
  s.addShape("rect", { x: 0, y: 4.55, w: 13.33, h: 2.95, fill: { color: COLOR.navyLight } });

  s.addText("DÉFI 2 · ÉCONOMIE NUMÉRIQUE · TOGO AI LAB", {
    x: 0.7, y: 0.9, w: 11.9, h: 0.4, fontFace: FONT_BODY, fontSize: 13,
    color: COLOR.amber, bold: true, charSpacing: 2, isTextBox: true,
  });
  s.addText("Adoption du numérique et inclusion\nfinancière par le mobile money", {
    x: 0.7, y: 1.5, w: 11.9, h: 2.2, fontFace: FONT_HEAD, fontSize: 40, bold: true,
    color: COLOR.white, isTextBox: true, lineSpacingMultiple: 1.05,
  });
  s.addText("Diagnostic de l'accès à Internet et aux services financiers, et recommandations pour accélérer l'inclusion numérique au Togo", {
    x: 0.7, y: 3.7, w: 9.5, h: 0.7, fontFace: FONT_BODY, fontSize: 15, italic: true,
    color: "C9D3E0", isTextBox: true,
  });

  const stats = [
    ["< 40 %", "de la population\nutilise Internet"],
    ["19 788", "agents mobile\nmoney recensés"],
    ["738", "établissements\nfinanciers référencés"],
  ];
  stats.forEach((st, i) => {
    const x = 0.7 + i * 4.1;
    s.addText(st[0], { x, y: 4.85, w: 3.7, h: 0.9, fontFace: FONT_HEAD, fontSize: 34, bold: true, color: COLOR.teal, isTextBox: true });
    s.addText(st[1], { x, y: 5.65, w: 3.7, h: 0.7, fontFace: FONT_BODY, fontSize: 12, color: "C9D3E0", isTextBox: true });
  });
}

// ---------------------------------------------------------------------------
// Slide 2 — Contexte & problématique
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.offwhite);
  s.addText("Le mobile money, porte d'entrée financière du Togo", {
    x: 0.6, y: 0.45, w: 12.1, h: 0.7, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: COLOR.navy, isTextBox: true,
  });
  s.addText(
    "Le mobile s'est imposé au Togo, mais l'accès à Internet et aux banques reste très inégal entre les territoires.",
    { x: 0.6, y: 1.15, w: 12.1, h: 0.5, fontFace: FONT_BODY, fontSize: 14, color: COLOR.gray, isTextBox: true }
  );

  const cards = [
    { n: "1", t: "Internet en retard", d: "37,6 % de la population utilisait Internet en 2022 — une progression rapide mais qui part de très bas." },
    { n: "2", t: "Banques concentrées", d: "Les établissements financiers classiques (banques, micro-finance, assurances) restent concentrés dans les zones urbaines." },
    { n: "3", t: "Mobile money dominant", d: "Près de 20 000 agents mobile money couvrent un territoire bien plus large que le réseau bancaire traditionnel." },
  ];
  cards.forEach((c, i) => {
    const x = 0.6 + i * 4.15;
    s.addShape("roundRect", { x, y: 2.05, w: 3.85, h: 4.6, rectRadius: 0.1, fill: { color: COLOR.white }, shadow: { type: "outer", color: "1A1A1A", opacity: 0.15, blur: 8, offset: 3, angle: 90 } });
    s.addShape("ellipse", { x: x + 0.35, y: 2.4, w: 0.7, h: 0.7, fill: { color: COLOR.teal } });
    s.addText(c.n, { x: x + 0.35, y: 2.4, w: 0.7, h: 0.7, align: "center", valign: "middle", fontFace: FONT_HEAD, fontSize: 22, bold: true, color: COLOR.white, isTextBox: true });
    s.addText(c.t, { x: x + 0.35, y: 3.3, w: 3.15, h: 0.5, fontFace: FONT_HEAD, fontSize: 16, bold: true, color: COLOR.navy, isTextBox: true });
    s.addText(c.d, { x: x + 0.35, y: 3.85, w: 3.15, h: 2.5, fontFace: FONT_BODY, fontSize: 12.5, color: COLOR.gray, isTextBox: true, lineSpacingMultiple: 1.2 });
  });
}

// ---------------------------------------------------------------------------
// Slide 3 — Évolution de l'usage Internet (line chart natif)
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.white);
  s.addText("Une croissance rapide, mais partie de très bas", {
    x: 0.6, y: 0.45, w: 12.1, h: 0.6, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: COLOR.navy, isTextBox: true,
  });
  s.addText("Part de la population togolaise utilisant Internet, 1996–2022", {
    x: 0.6, y: 1.05, w: 12.1, h: 0.4, fontFace: FONT_BODY, fontSize: 13, color: COLOR.gray, isTextBox: true,
  });

  const years = [1996, 1999, 2002, 2005, 2008, 2011, 2013, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022];
  const vals = [0.01, 0.59, 1.0, 1.8, 2.4, 3.5, 4.5, 7.12, 11.31, 12.36, 15.5, 20.73, 29.02, 32.51, 37.62];

  s.addChart(pres.ChartType.line, [{ name: "% population", labels: years.map(String), values: vals }], {
    x: 0.6, y: 1.6, w: 8.4, h: 5.2,
    showTitle: false, showLegend: false,
    lineSize: 3, lineDataSymbol: "circle", lineDataSymbolSize: 6,
    chartColors: [COLOR.teal],
    showValue: false,
    catAxisLabelColor: COLOR.gray, catAxisLabelFontSize: 10,
    valAxisLabelColor: COLOR.gray, valAxisLabelFontSize: 10,
    valAxisTitle: "% de la population", showValAxisTitle: true,
    valGridLine: { color: "E4E7EC", size: 1 },
    catGridLine: { style: "none" },
  });

  s.addShape("roundRect", { x: 9.3, y: 1.6, w: 3.45, h: 2.4, rectRadius: 0.08, fill: { color: COLOR.navy } });
  s.addText("+17 pts", { x: 9.55, y: 1.85, w: 3, h: 0.7, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: COLOR.amber, isTextBox: true });
  s.addText("gagnés entre 2019 et 2022 — la période la plus rapide d'accélération", { x: 9.55, y: 2.55, w: 2.95, h: 1.3, fontFace: FONT_BODY, fontSize: 12, color: "C9D3E0", isTextBox: true, lineSpacingMultiple: 1.2 });

  s.addShape("roundRect", { x: 9.3, y: 4.2, w: 3.45, h: 2.6, rectRadius: 0.08, fill: { color: COLOR.offwhite } });
  s.addText("Avant 2013 : quasi-stagnation sous les 5 %. La croissance ne décolle vraiment qu'avec la 3G/4G et la baisse du coût des smartphones.", {
    x: 9.55, y: 4.45, w: 2.95, h: 2.1, fontFace: FONT_BODY, fontSize: 12, color: COLOR.darkText, isTextBox: true, lineSpacingMultiple: 1.25,
  });
}

// ---------------------------------------------------------------------------
// Slide 4 — Marché des télécoms (stacked bar parts de marché)
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.white);
  s.addText("Un marché duopolistique, en léger rééquilibrage", {
    x: 0.6, y: 0.45, w: 12.1, h: 0.6, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: COLOR.navy, isTextBox: true,
  });
  s.addText("Parts de marché des opérateurs en % d'abonnés, 2013–2019", {
    x: 0.6, y: 1.05, w: 12.1, h: 0.4, fontFace: FONT_BODY, fontSize: 13, color: COLOR.gray, isTextBox: true,
  });

  const years = [2013, 2014, 2015, 2016, 2017, 2018, 2019];
  const atl = [45.43, 45.52, 45.97, 46.02, 48.48, 55.41, 48.56];
  const togocel = [54.57, 54.48, 54.03, 53.98, 51.52, 44.59, 51.44];

  s.addChart(
    pres.ChartType.bar,
    [
      { name: "Atlantique Telecom (Moov)", labels: years.map(String), values: atl },
      { name: "Togo Cellulaire (Togocom)", labels: years.map(String), values: togocel },
    ],
    {
      x: 0.6, y: 1.6, w: 7.6, h: 5.2, barGrouping: "stacked",
      chartColors: [COLOR.teal, COLOR.amber],
      showLegend: true, legendPos: "b", legendColor: COLOR.gray, legendFontSize: 11,
      showValue: false,
      catAxisLabelColor: COLOR.gray, catAxisLabelFontSize: 10,
      valAxisLabelColor: COLOR.gray, valAxisLabelFontSize: 10,
      valGridLine: { color: "E4E7EC", size: 1 }, catGridLine: { style: "none" },
    }
  );

  s.addText("Chiffre d'affaires du secteur", { x: 8.5, y: 1.6, w: 4.25, h: 0.4, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: COLOR.navy, isTextBox: true });
  const ca = [178.7, 188.1, 199.6, 187.6, 178.5, 177.2, 184.9]; // milliards FCFA (approx, /1000)
  s.addChart(pres.ChartType.line, [{ name: "CA (Md FCFA)", labels: years.map(String), values: ca }], {
    x: 8.5, y: 2.0, w: 4.25, h: 2.2, showLegend: false, showTitle: false,
    lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 4, chartColors: [COLOR.navy],
    catAxisLabelColor: COLOR.gray, catAxisLabelFontSize: 8, valAxisLabelColor: COLOR.gray, valAxisLabelFontSize: 8,
    valGridLine: { color: "E4E7EC", size: 1 }, catGridLine: { style: "none" },
  });

  s.addText("Télédensité mobile GSM", { x: 8.5, y: 4.35, w: 4.25, h: 0.4, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: COLOR.navy, isTextBox: true });
  const teledens = [55.87, 61.96, 66.78, 74.92, 82.98, 82.59, 81.91];
  s.addChart(pres.ChartType.bar, [{ name: "Télédensité mobile (%)", labels: years.map(String), values: teledens }], {
    x: 8.5, y: 4.75, w: 4.25, h: 2.05, showLegend: false, showTitle: false,
    chartColors: [COLOR.teal],
    catAxisLabelColor: COLOR.gray, catAxisLabelFontSize: 8, valAxisLabelColor: COLOR.gray, valAxisLabelFontSize: 8,
    valGridLine: { color: "E4E7EC", size: 1 }, catGridLine: { style: "none" },
  });
}

// ---------------------------------------------------------------------------
// Slide 5 — Cartographie de l'offre de services financiers
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.navy);
  s.addText("Le mobile money couvre un territoire bien plus large", {
    x: 0.6, y: 0.5, w: 12.1, h: 0.7, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: COLOR.white, isTextBox: true,
  });
  s.addText("Nombre de points d'accès géolocalisés, par région", {
    x: 0.6, y: 1.15, w: 12.1, h: 0.4, fontFace: FONT_BODY, fontSize: 13, color: "C9D3E0", isTextBox: true,
  });

  const regions = ["Maritime", "Plateaux", "Kara", "Savanes", "Centrale"];
  const mm = [8986, 3079, 2951, 2679, 2093];
  const fin = [364, 101, 80, 55, 62];

  s.addChart(
    pres.ChartType.bar,
    [
      { name: "Agents Mobile Money", labels: regions, values: mm },
      { name: "Établissements financiers (x20 pour lisibilité)", labels: regions, values: fin.map((v) => v * 20) },
    ],
    {
      x: 0.6, y: 1.75, w: 12.1, h: 5.0, barDir: "bar",
      chartColors: [COLOR.amber, COLOR.teal],
      showLegend: true, legendPos: "b", legendColor: "C9D3E0", legendFontSize: 11,
      catAxisLabelColor: "C9D3E0", catAxisLabelFontSize: 12,
      valAxisLabelColor: "C9D3E0", valAxisLabelFontSize: 10,
      valGridLine: { color: "2A3B5C", size: 1 }, catGridLine: { style: "none" },
    }
  );
}

// ---------------------------------------------------------------------------
// Slide 6 — Ratios d'inclusion financière par région
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.white);
  s.addText("Savanes : la région la moins bien desservie", {
    x: 0.6, y: 0.45, w: 12.1, h: 0.6, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: COLOR.navy, isTextBox: true,
  });
  s.addText("Habitants par point de service financier, par région (2022)", {
    x: 0.6, y: 1.05, w: 12.1, h: 0.4, fontFace: FONT_BODY, fontSize: 13, color: COLOR.gray, isTextBox: true,
  });

  const regions = ["Maritime", "Kara", "Centrale", "Plateaux", "Savanes"];
  const habAgent = [150, 334, 380, 531, 427];
  const habEtab = [3699, 12319, 12831, 16197, 20791];

  s.addChart(pres.ChartType.bar, [{ name: "Hab. / agent Mobile Money", labels: regions, values: habAgent }], {
    x: 0.6, y: 1.6, w: 5.9, h: 5.1, barDir: "bar",
    chartColors: [COLOR.teal], showLegend: false,
    showTitle: true, title: "Habitants / agent Mobile Money", titleFontSize: 13, titleColor: COLOR.navy,
    catAxisLabelColor: COLOR.gray, catAxisLabelFontSize: 11, valAxisLabelColor: COLOR.gray, valAxisLabelFontSize: 9,
    showValue: true, dataLabelColor: COLOR.navy, dataLabelFontSize: 10, dataLabelPosition: "outEnd",
    valGridLine: { color: "E4E7EC", size: 1 }, catGridLine: { style: "none" },
  });

  s.addChart(pres.ChartType.bar, [{ name: "Hab. / établissement financier", labels: regions, values: habEtab }], {
    x: 6.8, y: 1.6, w: 5.9, h: 5.1, barDir: "bar",
    chartColors: [COLOR.amber], showLegend: false,
    showTitle: true, title: "Habitants / établissement financier", titleFontSize: 13, titleColor: COLOR.navy,
    catAxisLabelColor: COLOR.gray, catAxisLabelFontSize: 11, valAxisLabelColor: COLOR.gray, valAxisLabelFontSize: 9,
    showValue: true, dataLabelColor: COLOR.navy, dataLabelFontSize: 10, dataLabelPosition: "outEnd",
    valGridLine: { color: "E4E7EC", size: 1 }, catGridLine: { style: "none" },
  });
}

// ---------------------------------------------------------------------------
// Slide 7 — Limites méthodologiques
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.offwhite);
  s.addText("Limites méthodologiques", {
    x: 0.6, y: 0.45, w: 12.1, h: 0.6, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: COLOR.navy, isTextBox: true,
  });

  const limits = [
    ["Pas de données de couverture réseau", "Aucune donnée ouverte 2G/3G/4G par zone n'est disponible pour le Togo — le ciblage géographique des investissements réseau reste approximatif."],
    ["Population au niveau canton", "Le recensement 2022 est publié au niveau canton/localité ; l'agrégation à la préfecture a été reconstituée et peut contenir de légers écarts."],
    ["Statuts d'usage déclaratifs", "Le statut d'activité des établissements financiers (« Utilisé », « Fermé », etc.) est déclaratif et daté de janvier 2025 ; une partie reste « Inconnu »."],
  ];
  limits.forEach((l, i) => {
    const y = 1.5 + i * 1.75;
    s.addShape("roundRect", { x: 0.6, y, w: 12.1, h: 1.5, rectRadius: 0.08, fill: { color: COLOR.white }, shadow: { type: "outer", color: "1A1A1A", opacity: 0.12, blur: 6, offset: 2, angle: 90 } });
    s.addShape("rect", { x: 0.6, y, w: 0.12, h: 1.5, fill: { color: COLOR.amber } });
    s.addText(l[0], { x: 1.05, y: y + 0.15, w: 11.3, h: 0.4, fontFace: FONT_HEAD, fontSize: 15, bold: true, color: COLOR.navy, isTextBox: true });
    s.addText(l[1], { x: 1.05, y: y + 0.6, w: 11.3, h: 0.8, fontFace: FONT_BODY, fontSize: 12.5, color: COLOR.gray, isTextBox: true, lineSpacingMultiple: 1.2 });
  });
}

// ---------------------------------------------------------------------------
// Slide 8 — Recommandations
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.white);
  s.addText("Cinq recommandations", {
    x: 0.6, y: 0.45, w: 12.1, h: 0.6, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: COLOR.navy, isTextBox: true,
  });

  const recos = [
    ["Prioriser Savanes", "Ratio habitants/établissement le plus élevé : l'impact marginal d'un nouveau point de service y est le plus fort."],
    ["Miser sur le mobile money", "Dans les préfectures sans établissement financier, étendre l'offre (épargne, micro-crédit) via les agents existants plutôt que d'attendre des agences physiques."],
    ["Publier les données de couverture réseau", "Une donnée ouverte 2G/3G/4G par zone permettrait un ciblage fin des investissements en infrastructure."],
    ["Encourager le multi-opérateur", "Réduire la dépendance des usagers à un seul opérateur mobile money renforce la résilience du service."],
    ["Suivre le ratio agents MM / établissements", "Un indicateur simple et déjà disponible pour mesurer chaque année la progression de l'inclusion financière."],
  ];

  recos.forEach((r, i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.6 + col * 6.2;
    const y = 1.35 + row * 1.85;
    const w = i === 4 ? 12.1 : 5.9;
    s.addShape("ellipse", { x, y, w: 0.55, h: 0.55, fill: { color: COLOR.teal } });
    s.addText(String(i + 1), { x, y, w: 0.55, h: 0.55, align: "center", valign: "middle", fontFace: FONT_HEAD, fontSize: 16, bold: true, color: COLOR.white, isTextBox: true });
    s.addText(r[0], { x: x + 0.7, y: y - 0.05, w: w - 0.7, h: 0.4, fontFace: FONT_HEAD, fontSize: 14.5, bold: true, color: COLOR.navy, isTextBox: true });
    s.addText(r[1], { x: x + 0.7, y: y + 0.38, w: w - 0.7, h: 1.15, fontFace: FONT_BODY, fontSize: 11.5, color: COLOR.gray, isTextBox: true, lineSpacingMultiple: 1.2 });
  });
}

// ---------------------------------------------------------------------------
// Slide 9 — Sources
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.offwhite);
  s.addText("Sources", {
    x: 0.6, y: 0.5, w: 12.1, h: 0.6, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: COLOR.navy, isTextBox: true,
  });
  const sources = [
    "Usage d'Internet — Part de la population, 1996–2022 (opendata.gouv.tg)",
    "Abonnés Internet — par type d'accès, technologie et opérateur, 2013–2019 (opendata.gouv.tg)",
    "Marché de la téléphonie — abonnés, télédensité, CA, investissements, 2013–2019 (opendata.gouv.tg)",
    "Établissements financiers géolocalisés — banques, micro-finance, assurances, mutuelles (opendata.gouv.tg)",
    "Agents mobile money géolocalisés (opendata.gouv.tg)",
    "Population résidente par découpage administratif — RGPH-5, 2022 (opendata.gouv.tg)",
  ];
  sources.forEach((src, i) => {
    s.addText("•  " + src, { x: 0.9, y: 1.5 + i * 0.55, w: 11.5, h: 0.5, fontFace: FONT_BODY, fontSize: 14, color: COLOR.darkText, isTextBox: true });
  });
}

// ---------------------------------------------------------------------------
// Slide 10 — Merci / clôture
// ---------------------------------------------------------------------------
{
  const s = pres.addSlide();
  bg(s, COLOR.navy);
  s.addText("Merci", {
    x: 0.7, y: 2.7, w: 11.9, h: 1.2, fontFace: FONT_HEAD, fontSize: 48, bold: true, color: COLOR.white, isTextBox: true,
  });
  s.addText("Défi 2 · Économie Numérique · Togo AI Lab", {
    x: 0.7, y: 3.9, w: 11.9, h: 0.5, fontFace: FONT_BODY, fontSize: 16, color: COLOR.amber, isTextBox: true,
  });
}

pres.writeFile({ fileName: "/home/claude/defi2-economie-numerique-togo/report/Defi2_Economie_Numerique_Togo.pptx" }).then(() => {
  console.log("PPTX généré avec succès.");
});
