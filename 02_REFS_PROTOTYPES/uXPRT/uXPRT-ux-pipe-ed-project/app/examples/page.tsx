"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { motion } from "framer-motion"

export default function ExamplesPage() {
  return (
    <div className="container py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-3xl font-bold mb-2">Real-World Examples</h1>
        <p className="text-muted-foreground">
          Learn from real-world product documentation examples
        </p>
      </motion.div>
      
      <Tabs defaultValue="gtm" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="gtm">Go-to-Market</TabsTrigger>
          <TabsTrigger value="onepager">One Pager</TabsTrigger>
          <TabsTrigger value="strategy">Product Strategy</TabsTrigger>
        </TabsList>
        <TabsContent value="gtm" className="pt-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Slack Launch GTM Plan</CardTitle>
                <CardDescription>
                  Example Go-to-Market plan for Slack's initial product launch
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  The GTM strategy for Slack focused on community-driven growth and word-of-mouth marketing.
                </p>
                <p className="mb-2"><strong>Key Components:</strong></p>
                <ul className="list-disc list-inside space-y-1 mb-4">
                  <li>Targeted beta program with tech-forward companies</li>
                  <li>Freemium model with generous free tier</li>
                  <li>Focus on user experience and delight</li>
                  <li>Integration marketplace to expand utility</li>
                </ul>
                <p className="mb-2"><strong>Results:</strong></p>
                <p>Slack grew to over 10 million daily active users primarily through word-of-mouth and limited marketing spend.</p>
              </CardContent>
            </Card>
          </motion.div>
        </TabsContent>
        <TabsContent value="onepager" className="pt-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Spotify Connect One Pager</CardTitle>
                <CardDescription>
                  Example of Spotify's one pager for the Connect feature
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  This one pager outlined the core problem and solution for Spotify Connect.
                </p>
                <p className="mb-2"><strong>Problem Statement:</strong></p>
                <p className="mb-4">
                  Users want to seamlessly switch their listening experience between devices without interruption or complex setup.
                </p>
                <p className="mb-2"><strong>Solution:</strong></p>
                <p className="mb-4">
                  Spotify Connect allows users to control music playing on any Spotify-enabled device from their phone, tablet, or desktop.
                </p>
                <p className="mb-2"><strong>Success Metrics:</strong></p>
                <ul className="list-disc list-inside space-y-1">
                  <li>50% of users utilizing multi-device playback weekly</li>
                  <li>20% reduction in session interruptions</li>
                  <li>15% increase in listening time</li>
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        </TabsContent>
        <TabsContent value="strategy" className="pt-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Netflix Personalization Strategy</CardTitle>
                <CardDescription>
                  Example of Netflix's product strategy for personalization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  Netflix's product strategy focused on creating a highly personalized viewing experience.
                </p>
                <p className="mb-2"><strong>Vision:</strong></p>
                <p className="mb-4">
                  To become the world's best entertainment distribution service by creating a personalized experience that helps members discover content they'll love.
                </p>
                <p className="mb-2"><strong>Key Strategy Components:</strong></p>
                <ul className="list-disc list-inside space-y-1 mb-4">
                  <li>Advanced recommendation algorithms</li>
                  <li>A/B testing infrastructure for rapid iteration</li>
                  <li>Content acquisition based on viewing patterns</li>
                  <li>Personalized UI elements (thumbnails, row order, etc.)</li>
                </ul>
                <p className="mb-2"><strong>Success Metrics:</strong></p>
                <p>Netflix estimates that its recommendation system saves the company $1 billion per year by reducing churn and increasing engagement.</p>
              </CardContent>
            </Card>
          </motion.div>
        </TabsContent>
      </Tabs>
    </div>
  )
}