from handlers.user.referral import router as referral_router
from aiogram import Dispatcher

# Add this to your router registration section:
# or however you import your dispatcher

dp = Dispatcher()  # or with your specific configuration
dp.include_router(referral_router)