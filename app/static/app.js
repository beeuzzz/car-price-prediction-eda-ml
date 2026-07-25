'use strict';

const LAYOUT = {
    'section-basic': [
        { kind: 'select', name: 'brand', required: true },
        { kind: 'number', name: 'production_year', label: 'Production year', required: true, step: 1, raw: true },
        { kind: 'number', name: 'mileage', label: 'Mileage', unit: 'km', required: true, step: 1000 },
        { kind: 'select', name: 'fuel_type', required: true }
    ],
    'section-technical': [
        { kind: 'number', name: 'engine_capacity', label: 'Engine capacity', unit: 'cm³', required: true, step: 1 },
        { kind: 'number', name: 'engine_power', label: 'Engine power', unit: 'HP', required: true, step: 1 },
        { kind: 'select', name: 'gearbox', required: true },
        { kind: 'select', name: 'drive', required: true },
        { kind: 'select', name: 'body_type', required: true },
        { kind: 'select', name: 'color', required: true }
    ],
    'section-sale': [
        { kind: 'select', name: 'voivodeship' },
        { kind: 'select', name: 'seller_type' }
    ]
};

const NUMERIC_FIELDS = ['production_year', 'mileage', 'engine_capacity', 'engine_power'];

let options = null;

const allFields = () => Object.values(LAYOUT).flat();
const fieldByName = (name) => allFields().find((field) => field.name === name);

const formatNumber = (value) => new Intl.NumberFormat('en-US').format(value);
const formatPln = (value) => formatNumber(value) + ' PLN';
const formatFieldNumber = (field, value) => (field.raw ? String(value) : formatNumber(value));

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
    const valueLabels = options.value_labels[field.name] || {};
    const label = field.label || options.category_labels[field.name] || field.name;

    const values = (options.categories[field.name] || [])
        .map((value) => ({ value, label: valueLabels[value] || value }))
        .sort((a, b) => a.label.localeCompare(b.label, 'en'));

    const wrapper = buildFieldShell(field, label);

    const select = document.createElement('select');
    select.id = field.name;
    select.name = field.name;

    const blank = document.createElement('option');
    blank.value = '';
    blank.textContent = field.required ? '— select —' : '— not specified —';
    select.appendChild(blank);

    for (const item of values) {
        const option = document.createElement('option');
        option.value = item.value;
        option.textContent = item.label;
        select.appendChild(option);
    }

    wrapper.appendChild(select);
    attachError(wrapper, field.name);
    return wrapper;
}

function buildNumber(field) {
    const range = options.ranges[field.name] || {};
    const wrapper = buildFieldShell(field, field.label || field.name);

    const input = document.createElement('input');
    input.type = 'number';
    input.id = field.name;
    input.name = field.name;
    if (range.min !== undefined) input.min = range.min;
    if (range.max !== undefined) input.max = range.max;
    if (field.step) input.step = field.step;

    if (range.min !== undefined) {
        const span = `${formatFieldNumber(field, range.min)} – ${formatFieldNumber(field, range.max)}`;
        input.placeholder = field.unit ? `${span} ${field.unit}` : span;
    }

    wrapper.appendChild(input);
    attachError(wrapper, field.name);
    return wrapper;
}

function buildEquipmentCheckboxes() {
    const container = document.getElementById('section-equipment');
    for (const item of options.equipment) {
        const label = document.createElement('label');
        label.className = 'checkbox';

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.dataset.equipment = item.name;
        input.id = 'eq_' + item.name;

        const text = document.createElement('span');
        text.textContent = item.label;

        label.append(input, text);
        container.appendChild(label);
    }
}

function buildImportedCheckbox() {
    const container = document.getElementById('section-sale');

    const wrapper = document.createElement('div');
    wrapper.className = 'field';

    wrapper.appendChild(buildLabel('imported', 'Origin'));

    const label = document.createElement('label');
    label.className = 'checkbox';

    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = 'imported';

    const text = document.createElement('span');
    text.textContent = 'Imported';

    label.append(input, text);
    wrapper.appendChild(label);
    container.appendChild(wrapper);
}

function setupEquipmentLevel() {
    const field = document.getElementById('equipment-level');
    const slider = document.getElementById('equipment_level');
    const output = document.getElementById('equipment_level_value');
    const skip = document.getElementById('equipment_level_skip');
    const presets = document.getElementById('equipment-presets');

    for (const preset of options.equipment_presets) {
        const button = document.createElement('button');
        button.type = 'button';
        button.textContent = `${preset.label} (${preset.value})`;
        button.addEventListener('click', () => {
            slider.value = preset.value;
            output.textContent = preset.value;
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
                setFieldError(field.name, field.kind === 'select' ? 'Select a value from the list.' : 'Enter a value.');
                firstInvalid = firstInvalid || element;
            }
            continue;
        }

        if (field.kind !== 'number') continue;

        const range = options.ranges[field.name] || {};
        const value = Number(raw);

        if (Number.isNaN(value)) {
            setFieldError(field.name, 'Enter a number.');
            firstInvalid = firstInvalid || element;
        } else if (value < range.min || value > range.max) {
            setFieldError(
                field.name,
                `The model supports the range ${formatFieldNumber(field, range.min)} – ${formatFieldNumber(field, range.max)}.`
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
    const payload = { equipment: {} };

    for (const field of allFields()) {
        const raw = document.getElementById(field.name).value.trim();
        if (raw === '') continue;

        payload[field.name] = NUMERIC_FIELDS.includes(field.name) ? Number(raw) : raw;
    }

    payload.imported = document.getElementById('imported').checked;

    for (const input of document.querySelectorAll('[data-equipment]')) {
        payload.equipment[input.dataset.equipment] = input.checked;
    }

    if (!document.getElementById('equipment_level_skip').checked) {
        payload.equipment_level = Number(document.getElementById('equipment_level').value);
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

    for (const entry of data.fields || []) {
        if (!fieldByName(entry.field) || !setFieldError(entry.field, entry.message)) {
            leftovers.push(`${entry.field}: ${entry.message}`);
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

    document.getElementById('result-price').textContent = formatPln(data.predicted_price);
    document.getElementById('result-range').textContent =
        `Likely range: ${formatPln(data.price_range.low)} – ${formatPln(data.price_range.high)}`;

    const warnings = document.getElementById('result-warnings');
    warnings.replaceChildren();
    for (const warning of data.warnings) {
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
    button.textContent = 'Calculating…';

    try {
        const response = await fetch('/api/v1/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(collectPayload())
        });

        const data = await response.json();

        if (response.ok) {
            showResult(data);
        } else if (data.fields) {
            showServerErrors(data);
        } else {
            showSummaryErrors([data.error || data.detail || 'Unknown server error']);
        }
    } catch (error) {
        showSummaryErrors(['Could not connect to the server: ' + error.message]);
    } finally {
        button.disabled = false;
        button.textContent = 'Estimate price';
    }
}

async function loadModelInfo() {
    const response = await fetch('/api/v1/model-info');
    if (!response.ok) return;

    const info = await response.json();
    const trained = new Date(info.train_timestamp).toLocaleDateString('en-US');

    document.getElementById('model-info').innerHTML =
        `Model <strong>${info.model_name}</strong>, ${info.input_feature_count} input features, ` +
        `trained on ${trained} on ${info.train_shape[0]} listings. ` +
        `Mean percentage error on the test set: <strong>${info.test_metrics.MAPE}%</strong> ` +
        `(MAE ${formatPln(info.test_metrics.MAE)}). The valuation is an estimate, not an offer.`;
}

function handleReset() {
    setTimeout(() => {
        clearErrors();
        document.getElementById('result').hidden = true;
        const slider = document.getElementById('equipment_level');
        document.getElementById('equipment_level_value').textContent = slider.value;
        document.getElementById('equipment_level_skip').dispatchEvent(new Event('change'));
    }, 0);
}

async function init() {
    try {
        const response = await fetch('/api/v1/form-options');
        if (!response.ok) throw new Error('server returned ' + response.status);
        options = await response.json();
    } catch (error) {
        showSummaryErrors(['Could not load the form configuration: ' + error.message]);
        return;
    }

    buildForm();

    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', handleSubmit);
    form.addEventListener('reset', handleReset);

    loadModelInfo();
}

init();
