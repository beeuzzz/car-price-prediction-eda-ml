'use strict';

const LAYOUT = {
    'section-basic': [
        { kind: 'select', name: 'marka', required: true },
        { kind: 'number', name: 'rok_produkcji', label: 'Rok produkcji', required: true, step: 1 },
        { kind: 'number', name: 'przebieg', label: 'Przebieg', unit: 'km', required: true, step: 1000 },
        { kind: 'select', name: 'paliwo', required: true }
    ],
    'section-technical': [
        { kind: 'number', name: 'pojemnosc_silnika', label: 'Pojemność silnika', unit: 'cm³', required: true, step: 1 },
        { kind: 'number', name: 'moc_silnika', label: 'Moc silnika', unit: 'KM', required: true, step: 1 },
        { kind: 'select', name: 'skrzynia_biegow', required: true },
        { kind: 'select', name: 'naped', required: true },
        { kind: 'select', name: 'nadwozie', required: true },
        { kind: 'select', name: 'kolor', required: true }
    ],
    'section-sale': [
        { kind: 'select', name: 'wojewodztwo' },
        { kind: 'select', name: 'typ_sprzedawcy' }
    ]
};

const NUMERIC_FIELDS = ['rok_produkcji', 'przebieg', 'pojemnosc_silnika', 'moc_silnika'];

let options = null;

const allFields = () => Object.values(LAYOUT).flat();
const fieldByName = (name) => allFields().find((field) => field.name === name);

const formatNumber = (value) => new Intl.NumberFormat('pl-PL').format(value);
const formatPln = (value) => formatNumber(value) + ' PLN';

function buildLabel(forId, text, { required = false } = {}) {
    const labelEl = document.createElement('label');
    labelEl.htmlFor = forId;
    labelEl.textContent = text;
    if (required) labelEl.classList.add('required');
    return labelEl;
}

function buildFieldShell(field, labelText) {
    const wrapper = document.createElement('div');
    wrapper.className = 'field';
    wrapper.dataset.field = field.name;

    wrapper.appendChild(buildLabel(field.name, labelText, { required: field.required }));

    return wrapper;
}

function attachError(wrapper, name) {
    const error = document.createElement('p');
    error.className = 'field-error';
    error.id = 'error_' + name;
    wrapper.appendChild(error);
}

function buildSelect(field) {
    const values = options.kategorie[field.name] || [];
    const valueLabels = options.etykiety_wartosci[field.name] || {};
    const label = field.label || options.etykiety_kategorii[field.name] || field.name;

    const wrapper = buildFieldShell(field, label);

    const select = document.createElement('select');
    select.id = field.name;
    select.name = field.name;

    const blank = document.createElement('option');
    blank.value = '';
    blank.textContent = field.required ? '— wybierz —' : '— nie podano —';
    select.appendChild(blank);

    for (const value of values) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = valueLabels[value] || value;
        select.appendChild(option);
    }

    wrapper.appendChild(select);
    attachError(wrapper, field.name);
    return wrapper;
}

function buildNumber(field) {
    const range = options.zakresy[field.name] || {};
    const wrapper = buildFieldShell(field, field.label || field.name);

    const input = document.createElement('input');
    input.type = 'number';
    input.id = field.name;
    input.name = field.name;
    if (range.min !== undefined) input.min = range.min;
    if (range.max !== undefined) input.max = range.max;
    if (field.step) input.step = field.step;

    if (range.min !== undefined) {
        const span = `${formatNumber(range.min)} – ${formatNumber(range.max)}`;
        input.placeholder = field.unit ? `${span} ${field.unit}` : span;
    }

    wrapper.appendChild(input);
    attachError(wrapper, field.name);
    return wrapper;
}

function buildEquipmentCheckboxes() {
    const container = document.getElementById('section-equipment');
    for (const item of options.wyposazenie) {
        const label = document.createElement('label');
        label.className = 'checkbox';

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.dataset.equipment = item.nazwa;
        input.id = 'eq_' + item.nazwa;

        const text = document.createElement('span');
        text.textContent = item.etykieta;

        label.append(input, text);
        container.appendChild(label);
    }
}

function buildImportedCheckbox() {
    const container = document.getElementById('section-sale');

    const wrapper = document.createElement('div');
    wrapper.className = 'field';

    wrapper.appendChild(buildLabel('importowany', 'Pochodzenie'));

    const label = document.createElement('label');
    label.className = 'checkbox';

    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = 'importowany';

    const text = document.createElement('span');
    text.textContent = 'Sprowadzony z zagranicy';

    label.append(input, text);
    wrapper.appendChild(label);
    container.appendChild(wrapper);
}

function setupEquipmentLevel() {
    const field = document.getElementById('equipment-level');
    const slider = document.getElementById('poziom_wyposazenia');
    const output = document.getElementById('poziom_wyposazenia_value');
    const skip = document.getElementById('poziom_wyposazenia_skip');
    const presets = document.getElementById('equipment-presets');

    for (const preset of options.presety_wyposazenia) {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = `${preset.etykieta} (${preset.wartosc})`;
        button.addEventListener('click', () => {
            slider.value = preset.wartosc;
            output.textContent = preset.wartosc;
        });
        presets.appendChild(button);
    }

    slider.addEventListener('input', () => {
        output.textContent = slider.value;
    });

    const applySkipState = () => {
        const skipped = skip.checked;
        slider.disabled = skipped;
        field.classList.toggle('is-disabled', skipped);
        for (const button of presets.querySelectorAll('button')) {
            button.disabled = skipped;
        }
        output.textContent = skipped ? '—' : slider.value;
    };

    skip.addEventListener('change', applySkipState);
    applySkipState();
}

function buildForm() {
    for (const [sectionId, fields] of Object.entries(LAYOUT)) {
        const section = document.getElementById(sectionId);
        for (const field of fields) {
            section.appendChild(field.kind === 'select' ? buildSelect(field) : buildNumber(field));
        }
    }

    buildImportedCheckbox();
    buildEquipmentCheckboxes();
    setupEquipmentLevel();
}

function clearErrors() {
    document.getElementById('errors').hidden = true;
    for (const element of document.querySelectorAll('.field-error')) {
        element.textContent = '';
    }
    for (const element of document.querySelectorAll('.field.has-error')) {
        element.classList.remove('has-error');
    }
}

function setFieldError(name, message) {
    const target = document.getElementById('error_' + name);
    if (!target) return false;

    target.textContent = message;
    target.closest('.field').classList.add('has-error');
    return true;
}

function validate() {
    let firstInvalid = null;

    for (const field of allFields()) {
        const element = document.getElementById(field.name);
        const raw = element.value.trim();

        if (raw === '') {
            if (field.required) {
                setFieldError(field.name, field.kind === 'select' ? 'Wybierz wartość z listy.' : 'Podaj wartość.');
                firstInvalid = firstInvalid || element;
            }
            continue;
        }

        if (field.kind !== 'number') continue;

        const range = options.zakresy[field.name] || {};
        const value = Number(raw);

        if (Number.isNaN(value)) {
            setFieldError(field.name, 'Podaj liczbę.');
            firstInvalid = firstInvalid || element;
        } else if (value < range.min || value > range.max) {
            setFieldError(
                field.name,
                `Model obsługuje zakres ${formatNumber(range.min)} – ${formatNumber(range.max)}.`
            );
            firstInvalid = firstInvalid || element;
        }
    }

    if (firstInvalid) {
        firstInvalid.focus();
        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    return firstInvalid === null;
}

function collectPayload() {
    const payload = { wyposazenie: {} };

    for (const field of allFields()) {
        const raw = document.getElementById(field.name).value.trim();
        if (raw === '') continue;

        payload[field.name] = NUMERIC_FIELDS.includes(field.name) ? Number(raw) : raw;
    }

    payload.importowany = document.getElementById('importowany').checked;

    for (const input of document.querySelectorAll('[data-equipment]')) {
        payload.wyposazenie[input.dataset.equipment] = input.checked;
    }

    if (!document.getElementById('poziom_wyposazenia_skip').checked) {
        payload.poziom_wyposazenia = Number(document.getElementById('poziom_wyposazenia').value);
    }

    return payload;
}

function showSummaryErrors(messages) {
    const box = document.getElementById('errors');
    const list = document.getElementById('errors-list');
    list.replaceChildren();

    for (const message of messages) {
        const item = document.createElement('li');
        item.textContent = message;
        list.appendChild(item);
    }

    box.hidden = false;
    document.getElementById('result').hidden = true;
    box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showServerErrors(data) {
    const leftovers = [];

    for (const entry of data.pola || []) {
        if (!fieldByName(entry.pole) || !setFieldError(entry.pole, entry.komunikat)) {
            leftovers.push(`${entry.pole}: ${entry.komunikat}`);
        }
    }

    if (leftovers.length) {
        showSummaryErrors(leftovers);
    } else {
        document.getElementById('result').hidden = true;
        document.querySelector('.field.has-error').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function showResult(data) {
    document.getElementById('errors').hidden = true;

    document.getElementById('result-price').textContent = formatPln(data.przewidywana_cena);
    document.getElementById('result-range').textContent =
        `Prawdopodobny zakres: ${formatPln(data.przedzial.od)} – ${formatPln(data.przedzial.do)}`;

    const warnings = document.getElementById('result-warnings');
    warnings.replaceChildren();
    for (const warning of data.ostrzezenia) {
        const item = document.createElement('li');
        item.textContent = warning;
        warnings.appendChild(item);
    }

    const box = document.getElementById('result');
    box.hidden = false;
    box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function handleSubmit(event) {
    event.preventDefault();
    clearErrors();

    if (!validate()) return;

    const button = document.getElementById('submit-button');
    button.disabled = true;
    button.textContent = 'Liczę…';

    try {
        const response = await fetch('/api/v1/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(collectPayload())
        });

        const data = await response.json();

        if (response.ok) {
            showResult(data);
        } else if (data.pola) {
            showServerErrors(data);
        } else {
            showSummaryErrors([data.blad || data.detail || 'Nieznany błąd serwera']);
        }
    } catch (error) {
        showSummaryErrors(['Nie udało się połączyć z serwerem: ' + error.message]);
    } finally {
        button.disabled = false;
        button.textContent = 'Wyceń pojazd';
    }
}

async function loadModelInfo() {
    const response = await fetch('/api/v1/model-info');
    if (!response.ok) return;

    const info = await response.json();
    const trained = new Date(info.train_timestamp).toLocaleDateString('pl-PL');

    document.getElementById('model-info').innerHTML =
        `Model <strong>${info.model_name}</strong>, ${info.liczba_cech_wejsciowych} cech wejściowych, ` +
        `wytrenowany ${trained} na ${info.train_shape[0]} ogłoszeniach. ` +
        `Średni błąd procentowy na zbiorze testowym: <strong>${info.metryki_testowe.MAPE}%</strong> ` +
        `(MAE ${formatPln(info.metryki_testowe.MAE)}). Wycena jest szacunkiem, nie ofertą.`;
}

function handleReset() {
    setTimeout(() => {
        clearErrors();
        document.getElementById('result').hidden = true;
        const slider = document.getElementById('poziom_wyposazenia');
        document.getElementById('poziom_wyposazenia_value').textContent = slider.value;
        document.getElementById('poziom_wyposazenia_skip').dispatchEvent(new Event('change'));
    }, 0);
}

async function init() {
    try {
        const response = await fetch('/api/v1/form-options');
        if (!response.ok) throw new Error('serwer zwrócił ' + response.status);
        options = await response.json();
    } catch (error) {
        showSummaryErrors(['Nie udało się pobrać konfiguracji formularza: ' + error.message]);
        return;
    }

    buildForm();

    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', handleSubmit);
    form.addEventListener('reset', handleReset);

    loadModelInfo();
}

init();
