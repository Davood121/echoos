// web_ui/src/components/BootAnim.jsx
import React, {useEffect} from 'react'
import { motion, useAnimation } from 'framer-motion'

export default function BootAnim({onComplete}){
  const controls = useAnimation()
  
  useEffect(()=>{
    async function sequence(){
      // Initial fade in and scale up
      await controls.start({
        opacity: 1, 
        scale: 1, 
        transition: { duration: 0.6, ease: "easeOut" }
      })
      
      // Rotate
      await controls.start({
        rotate: 360, 
        transition: { duration: 1.2, ease: "easeInOut" }
      })
      
      // Pulse / Settle
      await controls.start({
        scale: 0.9, 
        opacity: 0.9, 
        transition: { duration: 0.8 }
      })
      
      if(onComplete) onComplete()
    }
    sequence()
  }, [controls, onComplete])

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black z-50">
      <motion.div 
        initial={{opacity: 0, scale: 0.6}} 
        animate={controls} 
        className="w-48 h-48 rounded-2xl bg-gradient-to-br from-indigo-600 to-teal-400 shadow-2xl flex items-center justify-center"
      >
        <div className="text-white font-extrabold text-2xl tracking-widest">
          AURORA
        </div>
      </motion.div>
    </div>
  )
}
