import re

CSS = '/Users/yy/Documents/Curis AI Workspace/CONTENT_GROWTH_FULL_VISUAL_EXPLORATION/styles.css'
HTML = '/Users/yy/Documents/Curis AI Workspace/CONTENT_GROWTH_FULL_VISUAL_EXPLORATION/index.html'

with open(CSS, 'r', encoding='utf-8') as f:
    css = f.read()

# Token replacements (be careful with order to avoid double-substitution)
replacements = [
    # Root tokens
    ('--rail:#15161a;', '--rail:#3A4A52;'),
    ('--rail2:#1d1f26;', '--rail2:#4A5A62;'),
    ('--rail-line:#2a2d36;', '--rail-line:rgba(255,255,255,0.10);'),
    ('--bg:#f4f5f7;', '--bg:#F1EFDD;'),
    ('--surface:#ffffff;', '--surface:#FFFFFF;'),
    ('--surface2:#fafbfc;', '--surface2:#F5F4EA;'),
    ('--surface3:#f2f4f7;', '--surface3:#F5F4EA;'),
    ('--line:#e4e7ec;', '--line:#C5C5C1;'),
    ('--line2:#eef0f3;', '--line2:#E8E8E3;'),
    ('--t1:#171a1f;', '--t1:#090909;'),
    ('--t2:#5b6270;', '--t2:#5B616B;'),
    ('--t3:#8b929f;', '--t3:#8B929F;'),
    ('--t4:#aab0bb;', '--t4:#9CA3AF;'),
    ('--accent:#2f5bff;', '--accent:#8FB850;'),
    ('--accent-soft:#eef2ff;', '--accent-soft:rgba(143,184,80,0.12);'),
    ('--accent-line:#c9d5ff;', '--accent-line:rgba(143,184,80,0.35);'),
    ('--working:#2f5bff;', '--working:#8FB850;'),
    ('--wait:#8b929f;', '--wait:#8B929F;'),
    ('--review:#c07d10;', '--review:#B87922;'),
    ('--blocked:#d64545;', '--blocked:#C43F3F;'),
    ('--ready:#0f9d63;', '--ready:#1E7A5A;'),
    ('--unknown:#7a5af8;', '--unknown:#8B929F;'),
    ('--done:#0f9d63;', '--done:#1E7A5A;'),
    ('--human:#d97706;', '--human:#B87922;'),
    # Hardcoded rail colors
    ('background:#22252d;color:#e7eaf0', 'background:rgba(255,255,255,0.08);color:#F3EFED'),
    ('background:#2b2f3a;color:#fff;font-weight:600', 'background:rgba(143,184,80,0.22);color:#fff;font-weight:600'),
    ('background:#343a47;color:#cfd5df', 'background:rgba(255,255,255,0.15);color:#F3EFED'),
    ('background:#3d4553;color:#fff', 'background:rgba(143,184,80,0.30);color:#fff'),
    ('background:#1d2027;border-radius:8px', 'background:rgba(255,255,255,0.06);border-radius:8px'),
    ('background:#3b4250;color:#dfe4ec', 'background:#8FB850;color:#fff'),
    ('color:#c7ccd6;', 'color:#E8E8E3;'),
    ('color:#6f7683;', 'color:#9CA3AF;'),
    ('color:#7d848f;', 'color:#9CA3AF;'),
    ('color:#b6bcc7;', 'color:#E8E8E3;'),
    ('color:#e7eaf0;', 'color:#F3EFED;'),
    ('color:#a9b0bb;', 'color:#E8E8E3;'),
    ('border-bottom:1px solid var(--rail-line)', 'border-bottom:1px solid rgba(255,255,255,0.10)'),
    ('border-top:1px solid var(--rail-line)', 'border-top:1px solid rgba(255,255,255,0.10)'),
    # Focus green derived backgrounds (when old blue tint was hardcoded)
    ('background:#eef2ff;color:#2f5bff', 'background:rgba(143,184,80,0.10);color:#8FB850'),
    ('border-color:#dbe4ff', 'border-color:rgba(143,184,80,0.30)'),
    ('box-shadow:0 0 0 3px rgba(47,91,255,.08)', 'box-shadow:0 0 0 3px rgba(143,184,80,.15)'),
    ('border-color:#cfd5de;background:#fff', 'border-color:#B8B9B4;background:#fff'),
    ('background:#2449d6', 'background:#7A9E44'),
    ('border-left:3px solid var(--accent)', 'border-left:3px solid var(--accent)'),
    ('background:#22c55e', 'background:#8FB850'),
]

for old, new in replacements:
    css = css.replace(old, new)

# Update avatar / dot-live pulse to use soft green
css = re.sub(r'box-shadow:0 0 0 0 rgba\(34,197,94,', 'box-shadow:0 0 0 0 rgba(143,184,80,', css)
css = re.sub(r'box-shadow:0 0 0 6px rgba\(34,197,94,', 'box-shadow:0 0 0 6px rgba(143,184,80,', css)

with open(CSS, 'w', encoding='utf-8') as f:
    f.write(css)

# Clean index.html cache-busting query strings
with open(HTML, 'r', encoding='utf-8') as f:
    html = f.read()
html = re.sub(r'\?v=[a-f0-9]+"', '"', html)
with open(HTML, 'w', encoding='utf-8') as f:
    f.write(html)

print('Reskin complete')
