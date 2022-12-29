def get_duration(ctx):
    seconds = ctx.voice_client.source.duration % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hour > 0:
        duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
    else:
        duration = "%02dm %02ds" % (minutes, seconds)
    return duration
