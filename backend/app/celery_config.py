from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Investment
from .market_service import market_service
from datetime import datetime

celery_app = Celery('wealth_tracker', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(name='refresh_all_prices_midnight')
def refresh_all_investment_prices_midnight():
    db: Session = SessionLocal()
    try:
        print("🌙 Midnight price refresh started...")
        investments = db.query(Investment).all()
        symbols = list(set([inv.symbol for inv in investments]))
        
        if not symbols:
            return {"message": "No investments", "updated": 0}
        
        prices = market_service.get_multiple_prices(symbols)
        updated_count = 0
        
        for investment in investments:
            price_data = prices.get(investment.symbol)
            if price_data and price_data.get('price'):
                investment.last_price = price_data['price']
                investment.current_value = float(investment.units) * float(price_data['price'])
                investment.last_price_at = datetime.utcnow()
                updated_count += 1
        
        db.commit()
        print(f"✅ Midnight update complete: {updated_count} investments")
        return {"message": f"Updated {updated_count} investments", "updated": updated_count}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}
    finally:
        db.close()

celery_app.conf.beat_schedule = {
    'refresh-prices-at-midnight': {
        'task': 'refresh_all_prices_midnight',
        'schedule': crontab(hour=0, minute=0),
    },
}