with stg_crypto as (
    select * from {{ ref('stg_crypto_ohlcv') }}
),

daily_metrics as (
    select
        symbol,
        metric_date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        
        -- Calculate daily return
        (close_price - open_price) / open_price * 100 as daily_return_pct,
        
        -- Calculate price range
        high_price - low_price as daily_range,
        (high_price - low_price) / low_price * 100 as daily_range_pct,
        
        -- Previous day's close for comparison
        lag(close_price) over (partition by symbol order by metric_date) as prev_close,
        
        -- 7-day moving average
        avg(close_price) over (
            partition by symbol 
            order by metric_date 
            rows between 6 preceding and current row
        ) as ma_7day,
        
        -- 30-day moving average  
        avg(close_price) over (
            partition by symbol 
            order by metric_date 
            rows between 29 preceding and current row
        ) as ma_30day
        
    from stg_crypto
),

final as (
    select
        *,
        -- Day-over-day change
        case 
            when prev_close is not null 
            then (close_price - prev_close) / prev_close * 100 
        end as day_over_day_change_pct
    from daily_metrics
)

select * from final
