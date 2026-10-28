# Ověření podpory Codexu

Změna 0.5.1 navazuje na upstream 0.5.0 (`a9bbdade916293d6dd3be640a23e7c10cab96849`).
Ověřováno 28. 10. 2026 na macOS, Python 3.9.6, Node.js 25.9.0, npm 11.12.1 a Codex CLI 0.146.0.

## Rozsah změny

- Validní YAML hlavička skillu a instrukce použitelné v obou klientech.
- Nové projekty dostanou `AGENTS.md` se společnými pravidly a `CLAUDE.md`, který na něj odkazuje.
- Aktualizace doplní chybějící `AGENTS.md`; existující instrukce, rodinná data a nastavení náhledu zachová.
- Návody rozlišují dostupné nástroje prohlížeče a pomocných agentů. Při jejich absenci uvádějí náhradní postup.
- Genealogické nástroje a web zůstávají společné. Ve skriptech pro obrázky se změnilo jen znění zprávy o chybějícím ImageMagicku.

## Automatické regrese

Z kořene repozitáře:

```sh
python3 -m unittest discover -s tests -v
```

Šest testů prošlo: nový projekt, opakované založení beze změny obsahu, doplnění Codex instrukcí
starému projektu, zachování vlastních instrukcí a náhledu, záloha upraveného webu s aktualizací nástrojů
a kontrola konzistence ukázkových dat. Testy používají pouze standardní knihovnu a dočasné složky.

Skill prošel také validátorem `quick_validate.py` ze systémového skillu `skill-creator`.
Původní hlavička neprojde standardním YAML parserem, ale Codex CLI 0.146.0 ji při načítání toleruje;
oprava tedy není pro tuto konkrétní verzi blokující podmínkou načtení.

## Načtení a navázání v Codexu

- Přes skutečný `codex app-server` a požadavek `skills/list` byla ověřena kopie celého skillu
  v projektové `.agents/skills/rodokmen/`: `name=rodokmen`, `enabled=true`, bez chyby načtení.
- V této verzi se při stejném testu symlink složky skillu neobjevil v seznamu. Návod proto doporučuje kopii.
- Nová relace `codex exec --ephemeral --sandbox read-only` ve vygenerovaném projektu načetla skill,
  `data/STAV.md` a konec deníku. Bez zadání konkrétního názvu souboru v uživatelském promptu správně
  navázala na testovací sňatek `TEST-KNIHA-742`, zachovala nejistotu `prob` a uvedla chybějící snímek.
- Test používal vymyšlenou rodinu; nic nezveřejňoval a neměnil globální instalaci skillů.

## Opakování kontroly ukázkového webu

Ukázkový projekt prošel kontrolou konzistence, exportem a sestavením 587 stránek; Pagefind zaindexoval
všech 587 stránek. HTTP kontrola úvodu, osoby Jana Nováka, vějíře a hledání vrátila 200.
V prohlížeči se zobrazil úvod, ovládání vějíře i živé vyhledávací pole; kontrolované stránky neměly
chyby v konzoli. Dočasný server byl po testu zastaven.

Aktualizace byla ověřena také na projektu vytvořeném skutečným generátorem z `origin/main` 0.5.0.
SHA-256 všech souborů v `data/` zůstal shodný, doplnil se `AGENTS.md` a kontrola konzistence prošla.

Z kořene repozitáře (potřebuje přístup k registru npm):

```sh
SKILL_DIR="$PWD/skills/rodokmen"
DEMO_DIR="$(mktemp -d)"
python3 -I "$SKILL_DIR/tools/novy_projekt.py" "$DEMO_DIR" --ukazka
python3 -I "$DEMO_DIR/tools/kontrola.py"
npm --prefix "$DEMO_DIR/web" ci
npm --prefix "$DEMO_DIR/web" run data
ASTRO_TELEMETRY_DISABLED=1 npm --prefix "$DEMO_DIR/web" run build
npm --prefix "$DEMO_DIR/web" run preview
```

Náhled otevři na http://localhost:4321 a po ověření ukonči Ctrl+C. Nasazení není součást testu.
Proměnná u buildu brání Astro v zápisu telemetrického nastavení mimo testovací složku; v omezeném
prostředí byl tento zápis odmítnut. Pro instalaci balíčků byl potřeba povolený přístup k registru npm.

## Hranice ověření

Technické testy neprokazují správnost přepisu historického písma. Windows, nová relace Claude Code,
přihlášení a nasazení na Netlify ani všechny živé archivní portály nejsou tímto ověřením pokryté.
ImageMagick nebyl v testovacím prostředí dostupný; práci s výřezy je třeba ověřit po jeho instalaci.
