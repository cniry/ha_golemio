
"""Golemio integration init."""
from __future__ import annotations

from homeassistant import config_entries
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_TOKEN, CONF_NAME

DOMAIN = "golemio"
CONF_CONTAINERID = "container_id"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
	"""Set up the integration and migrate YAML configuration to config entries."""
	# Look for legacy YAML sensor platform configurations and import them
	sensor_configs = config.get("sensor", [])
	if not sensor_configs:
		return True

	# Existing entries to avoid duplicates
	existing = hass.config_entries.async_entries(DOMAIN)
	existing_container_ids = {entry.data.get(CONF_CONTAINERID) for entry in existing}

	for conf in sensor_configs:
		if conf.get("platform") != DOMAIN:
			continue
		name = conf.get(CONF_NAME)
		token = conf.get(CONF_TOKEN)
		containerid = conf.get(CONF_CONTAINERID)

		_LOGGER.debug("Found legacy golemio sensor in YAML: name=%s container_id=%s", name, containerid)

		if containerid in existing_container_ids:
			_LOGGER.info(
				"Skipping import for container_id=%s because a config entry already exists",
				containerid,
			)
			continue

		_LOGGER.info("Importing YAML golemio config for container_id=%s", containerid)

		# Start an import flow to create a config entry
		hass.async_create_task(
			hass.config_entries.flow.async_init(
				DOMAIN,
				context={"source": config_entries.SOURCE_IMPORT},
				data={
					CONF_NAME: name,
					CONF_TOKEN: token,
					CONF_CONTAINERID: containerid,
				},
			)
		)

	return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
	"""Set up Golemio from a config entry."""
	hass.data.setdefault(DOMAIN, {})
	hass.data[DOMAIN][entry.entry_id] = entry.data
	await hass.config_entries.async_forward_entry_setup(entry, "sensor")
	return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
	"""Unload a config entry."""
	unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
	if unload_ok:
		hass.data[DOMAIN].pop(entry.entry_id, None)
	return unload_ok

