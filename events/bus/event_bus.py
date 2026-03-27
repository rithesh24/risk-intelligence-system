import logging
from typing import Callable

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = {}
    
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.debug(f"[EventBus] Subscribed {handler.__name__} to {event_type}")
        
        
    def publish(self, event) -> None:
        event_type = type(event).__name__
        handlers = self.subscribers.get(event_type, [])
        
        if not handlers:
            logger.debug(f"[EventBus] No subscribers for {event_type}")
            return
        
        logger.debug(f"[EventBus] Publishing {event_type} to {len(handlers)} handler(s)")
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"[EventBus] Handler {handler.__name__} failed for {event_type}: {e}")
