def shotStats(rows, shotXmade): 
    """Compute stats relevant to shot chart."""
    
    threeMade = 0
    threeTotal = 0
    twoMade = 0
    twoTotal = 0
    
    # Compute Total field Goal Percentage
    fgp = 100 * len(shotXmade)/len(rows)
    fgp = "{:,.1f}%".format(fgp)
    
    # Count 2-Point, 3-Point totals
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            # determine if 3-Point shot or 2-Point shot
            if rows[i]["original_x"] <= -220 or rows[i]["original_x"] >= 220 or rows[i]["shot_distance"] >= 23.9:
                threeTotal += 1
                if rows[i]["event_type"] == "shot":
                    threeMade += 1
            else:
                twoTotal += 1
                if rows[i]["event_type"] == "shot":
                    twoMade += 1
        
    # Compute 3-Point Percentage
    threefgp = 100 * threeMade/threeTotal
    threefgp = "{:,.1f}%".format(threefgp)
    
    # Compute 2-Point Percentage
    twofgp = 100 * twoMade/twoTotal
    twofgp = "{:,.1f}%".format(twofgp)
    
    # Compute 3-Point Frequency
    threefreq = 100 * threeTotal/len(rows)
    threefreq = "{:,.1f}%".format(threefreq)
    
    # Compute 2-Point Frequency
    twofreq = 100 * twoTotal/len(rows)
    twofreq = "{:,.1f}%".format(twofreq)

    # Compute stats for shots in the paint
    paintMade = 0
    paintTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            # Determine if shots occur in paint
            if rows[i]["original_x"] >= -80 and rows[i]["original_x"] <= 80 and rows[i]["original_y"] <= 142.5:
                paintTotal += 1
                if rows[i]["event_type"] == "shot":
                    paintMade += 1
    
    # Compute Paint FG percentage
    paintfgp = 100 * paintMade/paintTotal
    paintfgp = "{:,.1f}%".format(paintfgp)
    
    # Compute Paint shot Frequency
    paintfreq = 100 * paintTotal/len(rows)
    paintfreq = "{:,.1f}%".format(paintfreq)
    
    # Compute Mid-range stats
    midrangeMade = 0
    midrangeTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            # Determine if shots are mid-range jumpers (not 3-pointer and not in paint)
            if not (rows[i]["original_x"] <= -220 or rows[i]["original_x"] >= 220 or rows[i]["shot_distance"] >= 23.9):  
                if not (rows[i]["original_x"] >= -80 and rows[i]["original_x"] <= 80 and rows[i]["original_y"] <= 142.5):
                    midrangeTotal += 1
                    if rows[i]["event_type"] == "shot":
                        midrangeMade += 1
        
    # Compute midrange FG percentage
    midrangefgp = 100 * midrangeMade/midrangeTotal
    midrangefgp = "{:,.1f}%".format(midrangefgp)
    
    # Compute midrange shot Frequency
    midrangefreq = 100 * midrangeTotal/len(rows)
    midrangefreq = "{:,.1f}%".format(midrangefreq)
    
    # Returns all calculated stats
    return {
        "totalFGP": fgp,
        "twoFGP": twofgp,
        "threeFGP": threefgp,
        "twoFreq": twofreq,
        "threeFreq": threefreq,
        "midrangeFGP": midrangefgp,
        "midrangeFreq": midrangefreq,
        "paintFGP": paintfgp,
        "paintFreq": paintfreq
    }
    
def assistStats(rows): 
    """Compute stats relevant to assist chart."""
    
    # Classify assisted shot as 2-Pointer or 3-Pointer
    twoTotal = 0
    threeTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            if rows[i]["original_x"] <= -220 or rows[i]["original_x"] >= 220 or rows[i]["shot_distance"] >= 23.9:
                threeTotal += 1
            else:
                twoTotal += 1
    
    # Compute 3-Point Frequency
    threefreq = 100 * threeTotal/len(rows)
    threefreq = "{:,.1f}%".format(threefreq)
    
    # Compute 2-Point Frequency
    twofreq = 100 * twoTotal/len(rows)
    twofreq = "{:,.1f}%".format(twofreq)
    
    # Compute stats for assisted shots in the paint
    paintMade = 0
    paintTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            # Determine if shots occur in paint
            if rows[i]["original_x"] >= -80 and rows[i]["original_x"] <= 80 and rows[i]["original_y"] <= 142.5:
                paintTotal += 1
            
    # Compute Paint shot Frequency
    paintfreq = 100 * paintTotal/len(rows)
    paintfreq = "{:,.1f}%".format(paintfreq)
    
    # Compute Midrange Frequency
    midrangefreq = 100 * (twoTotal - paintTotal)/len(rows)
    midrangefreq = "{:,.1f}%".format(midrangefreq)
    
    # Count Alley Oops
    alleyoopTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            if rows[i]["type"] == "Alley Oop Dunk":
                alleyoopTotal += 1
    
    # Compute Alley Oop Frequency
    alleyoopfreq = 100 * alleyoopTotal/len(rows)
    alleyoopfreq = "{:,.1f}%".format(alleyoopfreq)
    
    # Returns all calculated stats
    return {
        "twoFreq": twofreq,
        "threeFreq": threefreq,
        "midrangeFreq": midrangefreq,
        "paintFreq": paintfreq,
        "alleyoopFreq": alleyoopfreq
    }

def reboundStats(rows, orebX, drebX):
    """Compute stats relevant to rebound chart."""
    # Classify rebounded shot as 2-Pointer or 3-Pointer
    twoTotal = 0
    threeTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            if rows[i]["original_x"] <= -220 or rows[i]["original_x"] >= 220 or rows[i]["shot_distance"] >= 23.9:
                threeTotal += 1
            else:
                twoTotal += 1
    
    # Compute 3-Point Frequency
    threefreq = 100 * threeTotal/len(rows)
    threefreq = "{:,.1f}%".format(threefreq)
    
    # Compute 2-Point Frequency
    twofreq = 100 * twoTotal/len(rows)
    twofreq = "{:,.1f}%".format(twofreq)
    
    # Compute stats for rebounded shots in the paint
    paintMade = 0
    paintTotal = 0
    for i in range(len(rows)):
        if rows[i]["original_x"] != "unknown" and rows[i]["original_y"] != "unknown":
            # Determine if shots occur in paint
            if rows[i]["original_x"] >= -80 and rows[i]["original_x"] <= 80 and rows[i]["original_y"] <= 142.5:
                paintTotal += 1
            
    # Compute Paint shot Frequency
    paintfreq = 100 * paintTotal/len(rows)
    paintfreq = "{:,.1f}%".format(paintfreq)
    
    # Compute Midrange Frequency
    midrangefreq = 100 * (twoTotal - paintTotal)/len(rows)
    midrangefreq = "{:,.1f}%".format(midrangefreq)
    
    # Compute Offensive-Rebound Frequency
    orebfreq = 100 * len(orebX)/(len(orebX) + len(drebX))
    orebfreq = "{:,.1f}%".format(orebfreq)
    
     # Compute Defensive-Rebound Frequency
    drebfreq = 100 * len(drebX)/(len(orebX) + len(drebX))
    drebfreq = "{:,.1f}%".format(drebfreq)
    
    # Compute Offensive-Defensive Rebound ratio
    odratio = "{:,.1f}".format(len(orebX) / len(drebX))
    
    return {
        "twoFreq": twofreq,
        "threeFreq": threefreq,
        "midrangeFreq": midrangefreq,
        "paintFreq": paintfreq,
        "orebFreq": orebfreq,
        "drebFreq": drebfreq,
        "orebdrebRatio": odratio
    }