export const AVATAR_PRESETS = [["iris", "CEO", "#ede9fe", "#6d5bd0"], ["violet", "C", "#e8e2ff", "#5541bd"], ["amber", "Y", "#fff0d6", "#a45e13"], ["mint", "AI", "#dff5ec", "#217a5b"]];
export const avatarPreset = ref => AVATAR_PRESETS.find(([id]) => ref === `preset:${id}`) || null;
