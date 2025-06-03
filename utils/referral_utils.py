from sqlalchemy import select
from database.models import User
from datetime import datetime

async def notify_referrer_about_new_referral(bot, referrer_id, referred_username):
    """
    Send notification to referrer when someone uses their link
    
    Args:
        bot: Bot instance from aiogram
        referrer_id: Telegram ID of the user who shared the referral link
        referred_username: Username of the person who joined via the link
    """
    try:
        await bot.send_message(
            referrer_id,
            f"🎉 Хорошие новости! Пользователь @{referred_username or 'Anonymous'} "
            f"присоединился по вашей реферальной ссылке!"
        )
    except Exception as e:
        print(f"Failed to notify referrer {referrer_id}: {e}")


def generate_progress_bar(percentage, length=10):
    """
    Generate text-based progress bar
    
    Args:
        percentage: Number between 0-100 indicating progress
        length: Length of the bar in characters
        
    Returns:
        String with formatted progress bar
    """
    filled_length = int(length * percentage // 100)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}] {int(percentage)}%"


def check_referral_milestone(user):
    """
    Check if user has reached a new referral milestone
    
    Args:
        user: User object from database
        
    Returns:
        (has_new_milestone, num_new_rewards)
    """
    if not user.activated_referrals:
        return False, 0
        
    earned_rewards = user.activated_referrals // 15
    current_rewards = user.referral_rewards_earned or 0
    
    if earned_rewards > current_rewards:
        return True, earned_rewards - current_rewards
    return False, 0


async def track_referral_activation(bot, user_id, session):
    """
    Update referrer stats when user takes valuable action (e.g., subscribes)
    
    Args:
        bot: Bot instance from aiogram
        user_id: Telegram ID of user who completed an action
        session: SQLAlchemy async session
        
    Returns:
        None
    """
    user = await session.scalar(select(User).where(User.telegram_id == user_id))
    
    if not user or not user.referrer_id:
        return
    
    referrer = await session.scalar(select(User).where(User.telegram_id == user.referrer_id))
    if not referrer:
        return
    
    # Mark referral as activated if not already counted
    if user.is_activated_referral:
        return
        
    referrer.activated_referrals = (referrer.activated_referrals or 0) + 1
    user.is_activated_referral = True
    
    # Check if this activation grants a new reward
    has_new_milestone, new_rewards = check_referral_milestone(referrer)
    if has_new_milestone:
        referrer.referral_rewards_earned = (referrer.referral_rewards_earned or 0) + new_rewards
        
        # Notify referrer about new reward
        try:
            await bot.send_message(
                referrer.telegram_id,
                f"🎉 Поздравляем! Вы получили {new_rewards} "
                f"{'награду' if new_rewards == 1 else 'награды'} "
                f"за привлечение {referrer.activated_referrals} пользователей!"
            )
        except Exception as e:
            print(f"Failed to notify user {referrer.telegram_id}: {e}")
    
    await session.commit()


async def get_referral_link(bot, user_id):
    """
    Generate referral link for a user
    
    Args:
        bot: Bot instance from aiogram
        user_id: Telegram ID of the user
        
    Returns:
        String with formatted referral link
    """
    bot_username = (await bot.get_me()).username
    return f"https://t.me/{bot_username}?start={user_id}"