# Creates log2 plot comparing male to female depth for lines
# Copyright (C) 2014 Jessica Strein jessica.strein@uconn.edu
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

dir <- "/home/jessstrein/Storage/Results/DrosDel/depth_check/win_depth/sep_samples/"
fig_base <- "/home/jessstrein/Dropbox/chor_figs/"

male_file <- ""
female_file <- ""
filenames <- dir(path=dir, pattern="*_depth_10kb.tab.gz")
odds <- seq(1, length(filenames), 2)

read_num <- "/home/jessstrein/Storage/Data/DrosDel_data/refgenome/read_num_per_samp.tab"
r <- read.table(read_num,
                sep="\t",
                header=TRUE,
                stringsAsFactors=FALSE)

for(i in odds){
    x <- strsplit(filenames[i], "_")
    female_file <- paste(dir, filenames[i], sep="")
    print(female_file)
    f <- read.table(gzfile(female_file),
                    sep="\t",
                    header=TRUE,
                    na.strings="NA",
                    stringsAsFactors=FALSE)
    rfemale <- paste(x[[1]][1], "f", sep="_")
    male_file <- paste(dir, filenames[i+1], sep="")
    print(male_file)
    m <- read.table(gzfile(male_file),
                    sep="\t",
                    header=TRUE,
                    na.strings="NA",
                    stringsAsFactors=FALSE)
    rmale <- paste(x[[1]][1], "m", sep="_")
    print("working...")
    white <- c("2R", "3R", "2L", "3L", "4", "X")
    keeps <- data.frame()
    for(i in 1:length(m$chrom)) {
        tmp <- m[i,]
        if(tmp$chrom %in% white) {
            keeps <- rbind(keeps, tmp)
        }
    }
    femk <- data.frame()
    for(i in 1:length(f$chrom)) {
        tmp <- f[i,]
        if(tmp$chrom %in% white) {
            femk <- rbind(femk, tmp)
        }
    }
    for(a in 1:length(r$sample)){
        if(r$sample[a] == rmale){
            adjm <- r$read_count[a]
        } else if(r$sample[a] == rfemale){
            adjf <- r$read_count[a]
        }
    }
    adj_f_dp <- as.numeric(femk$mean_dp)/(adjf/100000)
    adj_m_dp <- as.numeric(keeps$mean_dp)/(adjm/100000)
    ratio <- log2(adj_m_dp/adj_f_dp)
    ln <- paste(x[[1]][1], "_log2.pdf", sep="")
    name <- paste(fig_base, ln, sep="")
    pdf(name, height=8, width=11)
    plot(ratio,
         xlab="Window position on chromosome",
         ylab="log2 ratio of male to female depth",
         pch=19)
    dev.off()
    male_file <- ""
    female_file <- ""
}

